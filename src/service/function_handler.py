import json
from enum import Enum

from src.model.functions import UseCaseFunctions, UseCase
from src.util.errors import FunctionNotFoundError, FunctionExecutionError, IllegalArgumentError


class FunctionHandlerService:
    """
    Service that provides the ability to call `use_case` specific functions using the 
    `handle_function` method. Before that, parse the arguments using the `parse_arguments` method.
    """

    def __init__(self, use_case: UseCase, function_set: dict) -> None:
        self.function_set = function_set

        self.use_case_functions = UseCaseFunctions(use_case, set(
            [fcn["name"] for fcn in function_set["functions"]]))

    def parse_arguments(self, function_name: str, arguments: dict) -> dict[str, str | int | float | bool | list]:
        """
        Parses the arguments against the predefined function_set function format.
        """
        parameter_details = self._get_parameter_details(
            function_name)
        required = self._get_required(function_name)

        out = dict()
        for arg_name, arg_value in arguments.items():

            if arg_name in parameter_details.keys():
                p_type, _ = parameter_details[arg_name]

                match p_type:
                    case "string": value = arguments.get(arg_name, default=None, type=str)
                    case "number": value = arguments.get(arg_name, default=None, type=int) if arg_value.isdecimal() else arguments.get(arg_name, default=None, type=float)
                    case "boolean": value = arguments.get(arg_name, default=None, type=bool)
                    case "array": value = arguments.getlist(arg_name)
                    case _: raise IllegalArgumentError(function_name, {arg_name})
                out.update({arg_name: value})
            else:
                # illegal/unexpected argument received
                raise IllegalArgumentError(function_name, {arg_name})

        if set(out.keys()).issuperset(required):
            return out

        # minimum required arguments were not provided
        raise IllegalArgumentError(
            function_name, arguments)

    def handle_function(self, function_name: str, function_args: dict) -> dict:
        """
        Use the use_case_functions object to call the underlying function. We expect them to return a dict formatted response.
        """

        try:
            return self.use_case_functions.call_function(function_name, function_args)
        except (FunctionExecutionError, FunctionNotFoundError) as e:
            raise e
        except json.JSONDecodeError:
            raise FunctionExecutionError(function_name, function_args)

    def _get_function(self, function_name: str) -> dict:
        """
        Return function from function_set with name function_name.
        """
        for function_set_fcn in self.function_set["functions"]:
            if function_name == function_set_fcn["name"]:
                return function_set_fcn

        raise FunctionNotFoundError(function_name, None)

    def _get_required(self, function_name: str) -> list[str]:
        """
        Returns the required list of arguments of the function with function_name.

        May raise FunctionNotFoundError.
        """

        fcn = self._get_function(function_name)
        return fcn["parameters"]["required"]

    def _get_parameter_details(self, function_name: str) -> dict[str: tuple[str, str]]:
        """
        Returns the parameter details of the specified function with function_name.

        p_type can be of either: string, number, boolean, array, as specified in the function_set.py

        # Can raise FunctionNotFoundError error.

        Returns:
            out (dict): A dict with parameter name as key and description and parameter type as tuple as value. 
        """
        fcn = self._get_function(function_name)

        out = dict()
        for p_name, p_info in fcn["parameters"]["properties"].items():
            p_type = p_info["type"]
            p_desc = p_info["description"]
            out.update({p_name: (p_type, p_desc)})

        return out
