import json
from typing import Dict

from src.model.functions import UseCaseFunctions, UseCase
from src.util.errors import FunctionNotFoundError, FunctionExecutionError, IllegalArgumentError


class FunctionHandlerService:
    """
    Service that provides the ability to call `use_case` specific functions using
    the `handle_function` method.
    """

    def __init__(self, use_case: UseCase, function_set: dict) -> None:
        function_names = set([fcn["name"]
                             for fcn in function_set["functions"]])
        self.function_set = function_set

        self.useCaseFunctions = UseCaseFunctions(use_case, function_names)

    def get_function(self, function_name: str):
        for function_set_fcn in self.function_set["functions"]:
            if function_name == function_set_fcn["name"]:
                return function_set_fcn

        return None

    def get_required(self, function_name: str) -> list[str]:
        fcn = self.get_function(function_name)
        return fcn["parameters"]["required"]

    def get_parameter_details(self, function_name: str) -> dict[str:tuple[str, bool, str]]:
        fcn = self.get_function(function_name)

        out = dict()
        for p_name, p_info in fcn["parameters"]["properties"].items():
            p_desc = p_info["description"]
            p_type = p_info["type"]
            out.update({p_name: (p_type, p_desc)})
        return out

    def parse_arguments(self, function_name: str, arguments: dict):

        parameter_details = self.get_parameter_details(function_name)
        required = self.get_required(function_name)
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
        else:
            # minimum required arguments were not provided
            raise IllegalArgumentError(
                function_name, {set(out.keys()).difference(required)})

    def handle_function(self, function_name: str, function_args: dict) -> json:
        try:
            return self.useCaseFunctions.call_function(function_name, function_args)
        except (FunctionExecutionError, FunctionNotFoundError) as e:
            # self._handle_error(e)
            print("ERROR")
            raise e  # TODO
        except json.JSONDecodeError:
            print("ERROR")
            raise FunctionExecutionError(function_name, function_args)

    # def _handle_error(error: FunctionNotFoundError | FunctionExecutionError, retry=3):  # TODO
    #     return FunctionErrorHandler(error.function_name, error.function_args, retry)
