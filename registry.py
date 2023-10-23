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

    @property
    def registered_functions(self):
        """Return the list of registered functions."""
        return self._functions
