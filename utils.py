from collections import namedtuple
from flask import request, jsonify

import regex as re

import json


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


def match_functions_with_metadata(functions, metadata_list):
    FunctionMetadataPair = namedtuple(
        'FunctionMetadataPair', ['function', 'meta_data'])

    function_dict = {func.name: func for func in functions}

    matched_metadata = {}

    for metadata in metadata_list:
        func_name = metadata.get('name')
        if func_name in function_dict:
            matched_metadata[func_name] = FunctionMetadataPair(
                function=function_dict[func_name],
                meta_data=metadata
            )
        else:
            print(f"No function found for metadata with name: {func_name}")

    return matched_metadata


def handle_function(cls, function, **kwargs) -> json:
    """Invoke function and return result"""
    try:
        return json.dumps(function(cls, **kwargs))
    except Exception as e:
        raise FunctionExecutionError(function, kwargs)


def extract_properties(metadata):
    properties_info = metadata.get('parameters', {}).get('properties', {})
    extracted_properties = {}

    for prop_name, prop_details in properties_info.items():
        prop_type = prop_details.get('type', 'unknown')
        extracted_properties[prop_name] = prop_type

    return extracted_properties


def convert_args(function_name, functions_and_metadata):
    try:
        metadata = functions_and_metadata.get(
            function_name).meta_data
    except KeyError as error:
        raise FunctionNotFoundError

    expected_properties = extract_properties(metadata)

    request_args = request.args.to_dict()

    converted_args = {}

    for arg_name, arg_value in request_args.items():
        expected_type = expected_properties.get(arg_name)

        if not expected_type:
            continue

        try:
            if expected_type == 'number':
                match_float = re.match("\d+.\d+", arg_value)
                if match_float:
                    converted_args[arg_name] = float(arg_value)
                else:
                    converted_args[arg_name] = int(arg_value)
            elif expected_type == 'string':
                converted_args[arg_name] = str(arg_value)
        except ValueError as e:
            return jsonify({"error": f"Invalid value for parameter '{arg_name}': {e}"}), 400

    return converted_args
