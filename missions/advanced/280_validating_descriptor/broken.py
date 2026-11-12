# Mission 280 - Config Field Descriptors
# Validating descriptors for typed configuration fields, with per-instance storage.

MISSING = object()


class Field:
    """Base descriptor: validates on assignment and stores the value on the instance."""

    def __init__(self, default=MISSING):
        self.default = default
        self.public = "<unbound>"
        self.storage = None
        self.value = default

    def __set_name__(self, owner, name):
        self.public = name
        self.storage = "_field"

    def validate(self, value):
        return value

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        try:
            return self.value
        except KeyError:
            if self.default is MISSING:
                raise AttributeError(f"{self.public} has not been set") from None
            return self.default

    def __set__(self, instance, value):
        self.value = self.validate(value)

    def __delete__(self, instance):
        instance.__dict__.pop(self.storage, None)


class IntRange(Field):
    def __init__(self, minimum, maximum, default=MISSING):
        super().__init__(default)
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.public} must be an int, got {type(value).__name__}")
        if not self.minimum <= value <= self.maximum:
            raise ValueError(f"{self.public} must be between {self.minimum} and {self.maximum}, got {value}")
        return value


class OneOf(Field):
    def __init__(self, *options, default=MISSING):
        super().__init__(default)
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"{self.public} must be one of {list(self.options)}, got {value!r}")
        return value


class Text(Field):
    def __init__(self, max_length=64, default=MISSING):
        super().__init__(default)
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.public} must be a string")
        value = value.strip()
        if not value:
            raise ValueError(f"{self.public} must not be blank")
        if len(value) > self.max_length:
            raise ValueError(f"{self.public} is longer than {self.max_length} characters")
        return value


class Model:
    def __init__(self, **values):
        for name, value in values.items():
            if not isinstance(getattr(type(self), name, None), Field):
                raise TypeError(f"unknown field {name!r}")
            setattr(self, name, value)

    @classmethod
    def fields(cls):
        found = {}
        for klass in reversed(cls.__mro__):
            for name, attr in vars(klass).items():
                if isinstance(attr, Field):
                    found[name] = attr
        return found

    def as_dict(self):
        return {name: getattr(self, name) for name in self.fields()}


class WorkerPool(Model):
    name = Text(32)
    size = IntRange(1, 64, default=4)
    mode = OneOf("thread", "process", default="thread")
    retries = IntRange(0, 10, default=3)


if __name__ == "__main__":
    pool = WorkerPool(name="ingest", size=8)
    print(pool.as_dict())
