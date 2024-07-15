class Signal:
    def __init__(self, *types):
        self.types = types
        self.func = None

    def __validate_types(self, *args, **kwargs):
        if (len(args) + len(kwargs.keys())) < len(self.types):
            raise TypeError(f"Not enough arguments (got {len(args) + len(kwargs.keys())}). Expected: {len(self.types)}")
        elif (len(args) + len(kwargs.keys())) > len(self.types):
            raise TypeError(f"Too many arguments (got {len(args) + len(kwargs.keys())}). Expected: {len(self.types)}")

        for i, arg in enumerate(args + tuple(kwargs.values())):
            if not isinstance(arg, self.types[i]):
                raise TypeError(f"Invalid argument '{arg}' at index {i} (type: {type(arg).__name__}). Expected type: {self.types[i].__name__}")

        return True

    def connect(self, func):
        self.func = func

    def emit(self, *args, **kwargs):
        if self.__validate_types(*args, **kwargs):
            if self.func is not None:
                return self.func(*args, **kwargs)
            else:
                print("Warning: No callback function connected")