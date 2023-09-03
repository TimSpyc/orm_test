import inspect

def kwargsDetails(func):
    sig = inspect.signature(func)
    result = {}
    for name, param in sig.parameters.items():
        result[name] = {
            'default': param.default if param.default != inspect.Parameter.empty else None,
            'annotation': param.annotation if param.annotation != inspect.Parameter.empty else None
        }
    return result

def identifyFunctionCaller():
    """
    Identifies the caller of the function that called this function. If the
    caller is a method, returns the instance of the class that called the
    method.
    """
    frame = inspect.currentframe()
    try:
        frame = frame.f_back.f_back
        if 'self' in frame.f_locals:
            instance = frame.f_locals['self']
            return instance
    finally:
        del frame # important to avoid memory leak!
