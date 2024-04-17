from flask import Flask, request, jsonify

from src.service.function_handler import FunctionHandlerService
from src.util.errors import IllegalArgumentError, FunctionExecutionError, FunctionNotFoundError
from src.util.use_case import UseCase


class FunctionServer:
    def __init__(self, host: str, port: int, use_case: UseCase, function_set: dict) -> None:
        self.host = host
        self.port = port

        self.function_handler = FunctionHandlerService(use_case, function_set)

    def start(self):
        app = Flask(f"Function Calling API Server")

        @app.route("/function_call/<function_name>", methods=["GET"])
        def function_call(function_name):
            try:
                function_args = self.function_handler.parse_arguments(
                    function_name, request.args)

                result = self.function_handler.handle_function(
                    function_name, function_args)

                return jsonify(result)

            except (FunctionExecutionError, FunctionNotFoundError, IllegalArgumentError) as e:
                print("Server error, when handling question: ", e)
                return jsonify({"error": str(e)}), 204

        app.run(host=self.host, port=self.port)
