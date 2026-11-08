REGISTRY = {}

def register_step(name, params=(), required=()):
    def decorator(func):
        REGISTRY[name] = {
            "func": func,
            "params": set(params),
            "required": set(required)
        }
        return func

    return decorator