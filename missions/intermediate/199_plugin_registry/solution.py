# Mission 199 - Sink Registry (solution)
# A decorator-based plugin registry for log sinks.
_REGISTRY = {}


def register(name):
    def decorator(cls):
        if name in _REGISTRY:
            raise ValueError(f"sink {name!r} is already registered")
        _REGISTRY[name] = cls
        return cls

    return decorator


def create(name, **options):
    try:
        sink_cls = _REGISTRY[name]
    except KeyError:
        known = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"unknown sink {name!r}; known sinks: {known}") from None
    return sink_cls(**options)


def clear_registry():
    _REGISTRY.clear()


@register("stdout")
class StdoutSink:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.lines = []

    def emit(self, message):
        self.lines.append(f"{self.prefix}{message}")


@register("webhook")
class WebhookSink:
    def __init__(self, url="http://localhost"):
        self.url = url
        self.sent = []

    def emit(self, message):
        self.sent.append((self.url, message))
