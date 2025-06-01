class CommandRegistry:
    _INSTANCE = None

    @classmethod
    def get_instance(cls):
        if not cls._INSTANCE:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self._registry = {}

    def register(self, key):
        def decorator(cls):
            self._registry[key] = cls
            return cls

        return decorator

    def create(self, key, *args, **kwargs):
        cls = self._registry.get(key)
        if not cls:
            raise ValueError(f"No class registered under key: {key}")
        return cls
