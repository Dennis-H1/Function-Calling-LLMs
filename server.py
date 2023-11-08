from flask import Flask, request, jsonify
import json

from music import Albums, Songs, all_functions
from utils import match_functions_with_metadata, convert_args, handle_function, FunctionExecutionError, FunctionNotFoundError

app = Flask(__name__)


# data and APIs
Albums.load_albums("./data/popular_albums.csv")
Songs.load_songs("./data/tracks.csv")

with open('functions.json', 'r') as file:
    function_metadata = json.load(file)

functions = match_functions_with_metadata(
    all_functions, function_metadata)


@app.route('/function_call/<function_name>', methods=['GET'])
def function_call(function_name):
    try:

        print(functions)

        converted_args = convert_args(function_name, functions)
    except FunctionNotFoundError as e:  # TODO conversion error
        return jsonify({"error": e}), 500

    class_method = functions[function_name].function
    cls = class_method.cls
    function = class_method.method

    try:
        result = handle_function(cls=cls, function=function, **converted_args)
        return jsonify({"result": result})
    except FunctionExecutionError as e:
        return jsonify({"error": e})


@app.route('/functions/all', methods=['GET'])
def functions_all():
    print(all_functions)
    return jsonify({"result": sorted([name for _, name, _ in all_functions])})


if __name__ == '__main__':
    app.run(debug=True)
