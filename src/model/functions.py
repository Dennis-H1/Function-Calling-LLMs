from src.util.use_case import UseCase
from src.util.errors import FunctionExecutionError, FunctionNotFoundError


class UseCaseFunctions:
    """
    Stores all usecase specific functions. The function_set provided in function_sets.json 
    stores the test run specific functions available to the LLM. They are a subset of all 
    available functions, but provide additional metadata (required for the LLM to interpret them).

    The `function_set_functions` are used to filter the `use_case` specific functions for usage.
    """

    def __init__(self, use_case: UseCase, function_set_functions: set[str]) -> None:
        match use_case:
            case UseCase.MUSIC:
                from src.model.music import MusicFunctions
                use_case_functions = MusicFunctions.functions

            case UseCase.TRAVEL_AND_RESTAURANTS:
                from src.model.travel_and_restaurants import TravelAndRestaurantFunctions
                use_case_functions = TravelAndRestaurantFunctions.functions

        self.available_functions: dict = {
            fcn.__name__: fcn for fcn in use_case_functions if fcn.__name__ in function_set_functions}

    def call_function(self, function_name: str, function_args: dict):
        fcn = self.available_functions.get(function_name)

        if fcn is None:
            raise FunctionNotFoundError(function_name, function_args)

        try:
            return fcn(**function_args)
        except Exception:
            FunctionExecutionError(function_name, function_args)
