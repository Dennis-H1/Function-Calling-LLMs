from flask import Flask, request, jsonify

from src.service.function_handler import FunctionHandlerService
from src.util.errors import IllegalArgumentError, FunctionExecutionError, FunctionNotFoundError
from src.util.use_case import UseCase


class FunctionServer:
    def __init__(self, host: str, port: int, use_case: UseCase, function_set: dict) -> None:
        self.host = host or "127.0.0.1"
        self.port = port or 5000

        self.function_handler = FunctionHandlerService(use_case, function_set)

    def start(self):
        app = Flask(__name__)

        @app.route("/", methods=["GET"])
        def hello():

            welcome_message = """
            <h1>Hello there</h1>,
            
            <p>
            The API endpoints are:
            <ul>
                <li>/shutdown to shutdown the server </li>
                <li>/function_call/function=<function_name>&arg1=<arg1>... to run function calls. </li>
            <ul> 
            </p>
            
            <p>
                Check out the github and src/config folder to configure test runs.
            </p>
            """
            return welcome_message

        @app.route("/function_call/<function_name>", methods=["GET"])
        def function_call(function_name):
            try:
                function_args = self.function_handler.parse_arguments(
                    function_name, request.args)
                result = self.function_handler.handle_function(
                    function_name, function_args)

                import pprint
                # pprint.pprint(result)

                print(function_args)

                return jsonify(result)
            except (FunctionExecutionError, FunctionNotFoundError) as e:
                print("FUNCTION_ERROR")
                return jsonify({"error": str(e)}), 204
            except IllegalArgumentError as e:
                print("ILLEGALARGUMENTERROR")
                return jsonify({"error": str(e)}), 204

        app.run(host=self.host, port=self.port)
