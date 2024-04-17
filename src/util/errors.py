class FunctionNotFoundError(Exception):
    def __init__(self, function_name, function_args):
        self.function_name = function_name
        self.function_args = function_args
        super().__init__(
            f"Error finding function {function_name} with arguments {function_args}")


class FunctionExecutionError(Exception):
    def __init__(self, function_name, function_args):
        self.function_name = function_name
        self.function_args = function_args
        super().__init__(
            f"Error executing function {function_name} with arguments {function_args}")


class IllegalArgumentError(Exception):
    def __init__(self, function_name, function_args):
        self.function_name = function_name
        self.function_args = function_args
        super().__init__(
            f"Error parsing arguments {function_args} for function {function_name}.")


class ServerResponseError(Exception):
    def __init__(self):
        super().__init__(
            f"Error received from Server. This could entail that the function was not found or wrong arguments were passed.")
