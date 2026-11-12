# Mission 094 - Subclass Lost Its Parent (solution)
# Database instance types built on a shared base class.


class Instance:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.tags = []

    def label(self):
        return f"{self.name}@{self.region}"


class PostgresInstance(Instance):
    def __init__(self, name, region, version):
        super().__init__(name, region)
        self.version = version

    def describe(self):
        return f"{self.label()} postgres {self.version}"


class RedisInstance(Instance):
    def __init__(self, name, region, memory_mb):
        super().__init__(name, region)
        self.memory_mb = memory_mb

    def describe(self):
        return f"{self.label()} redis {self.memory_mb}MB"


def tag(instance, key):
    instance.tags.append(key)
    return instance.tags


if __name__ == "__main__":
    print(PostgresInstance("pg-main", "eu-1", "15").describe())
    print(RedisInstance("cache-1", "us-2", 512).describe())
