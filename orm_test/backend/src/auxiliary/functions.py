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