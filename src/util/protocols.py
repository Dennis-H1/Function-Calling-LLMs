from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ModelSolution:
    functions: list[dict]
    parameters: list[dict]
    answer: str


class LLMService(ABC):
    """
    Abstract base class for a Large Language Model (LLM) service.
    This class defines a standardized interface for interacting with different LLMs.
    """

    def __init__(self, api_key: str, function_set: dict, prompt: str, model: str, hyperparameters: dict) -> None:
        """
        Initializes the LLM service with necessary configuration.

        Args:
            api_key (str): API key for the LLM service.
            function_set (dict): Set of functions the LLM can perform.
            prompt (str): Initial text or context to set up the LLM.
            model (str): Specific model identifier.
            hyperparameters (dict): Hyperparameters like temperature, max tokens, etc.
        """
        self.api_key = api_key
        self.function_set = function_set
        self.prompt = prompt
        self.model = model
        self.hyperparameters = hyperparameters

    @abstractmethod
    def process_question(self, question: str) -> tuple[ModelSolution, int, int]:
        """
        Processes a question through the LLM and retrieves the model solution.

        The following errors must be handled:
            - src.util.errors.ServerResponseError
            - any LLM specific errors

        if an error is caught, return (None, 0, 0), which is caught by pipeline.

        Args:
            question (str): The question to process.

        Returns:
            ModelSolution: The LLM's response to the question. Or None, if error occured during processing.
            int: The number of received tokens.
            int: The number of sent tokens.
        """
        pass

    @abstractmethod
    def _handle_function(self, function_call: dict) -> str:
        """
        Make a HTTP request to the API Server.

        Args:
            function_call (dict): The function call details. The name and parameters are required.

        Use the src.util.request.server_request function to make server calls for function handling.

        Returns:
            str: The function call result.
        """
        pass
