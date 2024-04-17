from __future__ import annotations
import re
import json

import openai
import openai.error
from tiktoken import get_encoding

from src.util.errors import ServerResponseError
from src.util.protocols import LLMService, ModelSolution
from src.util.request import server_request


class GPTService(LLMService):

    MAX_ITERATIONS = 10

    class Response:
        def __init__(self, message: dict):
            self._message = message

        @classmethod
        def from_api(cls, openai_response):
            _message = openai_response["choices"][0]["message"]
            return cls(_message)

        @property
        def message(self) -> str:
            return self._message["content"]

        @property
        def role(self) -> str:
            return self._message["role"]

        @property
        def function_call(self) -> dict:
            return self._message.get("function_call")

        @property
        def is_function_call(self) -> bool:
            return self.function_call is not None

        @property
        def tool_calls(self) -> dict:
            return self._message.get("tool_calls")

        @property
        def is_tool_call(self) -> bool:
            return self.tool_calls is not None

        def to_dict(self) -> dict:
            return {**self._message}

        def __str__(self) -> str:
            return f"Response({self.role}: {self.message}, with function:{self.function_call})"

    class Conversation:
        def __init__(self):
            self._messages = []

        @property
        def messages_as_dicts(self) -> list[dict]:
            return [message.to_dict() for message in self._messages]

        def send(self, model, functions, temperature, mode) -> GPTService.Response:
            args = {"model": model,
                    "temperature": temperature,
                    "messages": self.messages_as_dicts}

            if len(functions) > 0:
                if mode == "sequential":
                    args.update({"function_call": "auto",
                                "functions": functions})

                elif mode == "parallel":
                    tools = [{"type": "function", "function": function}
                             for function in functions]
                    args.update({"tool_choice": "auto", "tools": tools})

            response = openai.ChatCompletion.create(**args)
            return GPTService.Response.from_api(response)

        def add(self, message_or_response):
            if isinstance(message_or_response, GPTService.Response):
                message = message_or_response
            else:
                message = GPTService.Response(message_or_response)

            self._messages.append(message)
            return self

        def __str__(self) -> str:
            return f"{self.messages_as_dicts}"

    def __init__(self, api_key: str, function_set: dict, prompt: str, model: str, hyperparameters: dict) -> None:
        super().__init__(api_key, function_set, prompt, model, hyperparameters)

        openai.api_key = api_key
        self.temperature = hyperparameters["temperature"]
        self.mode = hyperparameters["mode"]

    def process_question(self, question: str) -> tuple[ModelSolution, int, int]:
        conversation = GPTService.Conversation()
        conversation.add({"role": "system", "content": self.prompt})
        conversation.add({"role": "user", "content": question})

        try:
            self._chat(conversation)
            final_response = conversation.messages_as_dicts[-1]["content"]
            final_response = re.sub('"', "'", final_response, flags=re.M)

        except (Exception) as e:
            return None, 0, 0

        function_names, function_arguments = self._extract_function_calls(
            conversation, self.mode)

        tokens_in, tokens_out = self._get_tokens_from_conversation(
            conversation)

        return ModelSolution(function_names, function_arguments, final_response), tokens_in, tokens_out

    def _handle_function(self, function_call: dict):
        function_name = function_call["name"]
        arguments = json.loads(function_call["arguments"])

        try:
            return server_request(function_name, arguments)
        except ServerResponseError:
            raise ServerResponseError

    def _chat(self, conversation: Conversation) -> None:
        for _ in range(GPTService.MAX_ITERATIONS):
            response = conversation.send(
                self.model, self.function_set["functions"], self.temperature, self.mode)
            conversation.add(response)

            if self.mode == "sequential" and response.is_function_call:
                try:
                    result = self._handle_function(response.function_call)
                    conversation.add(
                        {"role": "function", "content": result, "name": response.function_call["name"]})
                except ServerResponseError as error:
                    raise error

            elif self.mode == "parallel" and response.is_tool_call:
                for tool_call in response.tool_calls:
                    try:
                        result = self._handle_function(
                            tool_call["function"])
                        conversation.add({"role": "tool", "content": result,
                                          "name": tool_call.function.name, "tool_call_id": tool_call.id})
                    except ServerResponseError as error:
                        raise error
            else:
                return

    def _extract_function_calls(self, conversation: Conversation, mode: str):
        function_arguments = []
        function_names = []

        if mode == "parallel":
            tool_calls = [message.get("tool_calls")
                          for message in conversation.messages_as_dicts]
            for tool_calls in tool_calls:
                if tool_calls:
                    for tool_call in tool_calls:
                        function_names.append(tool_call["function"]["name"])
                        function_arguments.append(json.loads(
                            tool_call["function"]["arguments"]))

        elif mode == "sequential":
            function_calls = [message.get("function_call")
                              for message in conversation.messages_as_dicts]
            function_names = [func_call["name"]
                              for func_call in function_calls if func_call]
            function_arguments = [json.loads(
                func_call["arguments"]) for func_call in function_calls if func_call]

        return function_names, function_arguments

    def _get_tokens(self, string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def _get_tokens_from_conversation(self, conversation: Conversation) -> tuple[int, int]:
        client_inputs = "".join([str(message) for message in conversation.messages_as_dicts if message["role"] ==
                                "user" or message["role"] == "system" or message["role"] == "tool" or message["role"] == "function"])

        llm_outputs = "".join([
            str(message) for message in conversation.messages_as_dicts if message["role"] == "assistant"])

        tokens_in = self._get_tokens(client_inputs)
        tokens_out = self._get_tokens(llm_outputs)

        return tokens_in, tokens_out
