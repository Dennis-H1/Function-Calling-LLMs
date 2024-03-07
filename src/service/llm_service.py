import re
import json
import openai
import requests
from enum import Enum
from tiktoken import get_encoding

from src.util.errors import FunctionNotFoundError, FunctionExecutionError

MAX_ITERATIONS = 15


class Role(Enum):
    ASSISTANT = "assistant"
    FUNCTION = "function"
    SYSTEM = "system"
    USER = "user"
    TOOL = "tool"


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

    def __str__(self):
        return f"Response({self.role}: {self.message}, with function:{self.function_call})"


class Conversation:
    def __init__(self):
        self._messages = []

    @property
    def messages_as_dicts(self) -> list[dict]:
        return [message.to_dict() for message in self._messages]

    def send(self, model, functions, temperature, mode) -> Response:
        args = {"model": model,
                "temperature": temperature,
                "messages": self.messages_as_dicts}

        if len(functions) > 0:
            if mode == "sequential":
                args.update({"function_call": "auto", "functions": functions})

            elif mode == "parallel":
                tools = [{"type": "function", "function": function}
                         for function in functions]
                args.update({"tool_choice": "auto", "tools": tools})

        response = openai.ChatCompletion.create(**args)
        return Response.from_api(response)

    def add(self, message_or_response):
        if isinstance(message_or_response, Response):
            message = message_or_response
        else:
            message = Response(message_or_response)

        self._messages.append(message)
        return self

    def __str__(self):
        return f"{self.messages_as_dicts}"


class LLMService():

    def __init__(self, function_set: dict, prompt: str, model: str, hyperparameters: dict, mode: str, api_key: str) -> None:

        openai.api_key = api_key

        self.function_set = function_set
        self.prompt = prompt
        self.model = model
        self.hyperparameters = hyperparameters
        self.temperature = 0  # TODO
        self.mode = mode  # TODO: test for parallel

    def start_chat(self, conversation: Conversation) -> tuple[str, Conversation]:
        for _ in range(MAX_ITERATIONS):
            response = conversation.send(
                self.model, self.function_set["functions"], self.temperature, self.mode)
            conversation.add(response)

            if self.mode == "sequential" and response.is_function_call:
                try:
                    result = self.handle_function(response.function_call)
                    conversation.add(
                        {"role": Role.FUNCTION.value, "content": result, "name": response.function_call["name"]})
                except (FunctionNotFoundError, FunctionExecutionError) as error:
                    self.handle_error(error=error, retry=False)

            elif self.mode == "parallel" and response.is_tool_call:
                for tool_call in response.tool_calls:
                    try:
                        result = self.handle_function(
                            response.function_call)
                        conversation.add({"role": Role.TOOL.value, "content": result,
                                          "name": tool_call.function.name, "tool_call_id": tool_call.id})
                    except (FunctionNotFoundError, FunctionExecutionError) as error:
                        self.handle_error(error=error, retry=False)
            else:
                return response.message, conversation

    def handle_function(self, function_call: dict):
        function_name = function_call["name"]
        arguments = json.loads(function_call["arguments"])

        try:
            response = requests.get(
                f"http://127.0.0.1:5000/function_call/{function_name}", arguments, timeout=5)
            return response.content.decode(encoding="utf-8")

        except requests.ConnectionError as e:
            raise e  # TODO exceptions

    def handle_error(self):
        raise NotImplementedError

    def process_question_parallel(self, conversation: Conversation):
        function_arguments = []
        function_names = []

        tool_calls = [message.get("tool_calls")
                      for message in conversation.messages_as_dicts]
        for tool_calls in tool_calls:
            if tool_calls:
                for tool_call in tool_calls:
                    function_names.append(tool_call["function"]["name"])
                    function_arguments.append(json.loads(
                        tool_call["function"]["arguments"]))

        return function_names, function_arguments

    def process_question_sequential(self, conversation: Conversation):
        function_calls = [message.get("function_call")
                          for message in conversation.messages_as_dicts]
        function_names = [func_call["name"]
                          for func_call in function_calls if func_call]
        function_arguments = [json.loads(
            func_call["arguments"]) for func_call in function_calls if func_call]

        return function_names, function_arguments

    def process_question(self, question) -> tuple[str, list[dict], list[dict], int, int, Conversation]:
        conversation = Conversation()
        conversation.add({"role": Role.SYSTEM.value, "content": self.prompt})
        conversation.add({"role": Role.USER.value, "content": question})

        try:
            self.start_chat(conversation)
            final_response = conversation.messages_as_dicts[-1]["content"]
            final_response = re.sub('"', "'", final_response, flags=re.M)

        except (ValueError, FunctionExecutionError, FunctionNotFoundError) as e:  # TODO error messages
            print(f"Failed to answer due to error: {e}")
            final_response = None

        # interpret results
        if self.mode == "parallel":
            function_names, function_arguments = self.process_question_parallel(
                conversation)
        else:
            function_names, function_arguments = self.process_question_sequential(
                conversation)

        return final_response, function_names, function_arguments, conversation

    def get_tokens(self, string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def get_tokens_from_conversation(self, conversation: Conversation) -> tuple[int, int]:
        client_inputs = "".join([str(message) for message in conversation.messages_as_dicts if message["role"] ==
                                Role.USER.value or message["role"] == Role.SYSTEM.value or message["role"] == Role.TOOL.value or message["role"] == Role.FUNCTION.value])

        llm_outputs = "".join([
            str(message) for message in conversation.messages_as_dicts if message["role"] == Role.ASSISTANT.value])

        tokens_in = self.get_tokens(client_inputs)
        tokens_out = self.get_tokens(llm_outputs)

        return tokens_in, tokens_out
