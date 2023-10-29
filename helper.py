import json
from functools import wraps


class Registry:
    def __init__(self):
        self._functions = {}

    def register(self, func):
        """Decorator to register a function."""
        self._functions[func.__name__] = func
        return func

    def __contains__(self, name):
        return name in self._functions.keys()

    def __getitem__(self, name):
        return self._functions.get(name)

    def clear_register(self):
        del self._functions
        self._functions = {}

    @property
    def registered_functions(self):
        """Return the list of registered functions."""
        return self._functions


def to_json(fcn):
    @wraps(fcn)
    def wrapper(*args, **kwargs):
        result = fcn(*args, **kwargs)
        return json.dumps(result)
    return wrapper
