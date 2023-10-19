import inspect


def generate_function_metadata(func):
    # Extract the function signature
    sig = inspect.signature(func)
    params = sig.parameters

    # Initialize the dictionary structure
    metadata = {
        "name": func.__name__,
        "description": func.__doc__.strip(),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }

    # Populate properties and required fields based on function parameters
    for name, param in params.items():
        param_details = {
            "type": "string",  # Default type, can be modified based on annotations
        }

        # Check if parameter has a default value
        if param.default != inspect.Parameter.empty:
            param_details["default"] = param.default
        else:
            metadata["parameters"]["required"].append(name)

        # TODO: You can expand this logic to handle custom annotations for parameter types and descriptions

        metadata["parameters"]["properties"][name] = param_details

    return metadata


# Example usage:
def get_current_weather(location: str, other: int, unit: str = "fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return weather_info


from pprint import pprint

pprint(generate_function_metadata(get_current_weather))
