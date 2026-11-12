# Mission 119 - Replica Count Validator
# Validates user-supplied deployment settings before building a manifest.
ENVIRONMENTS = ("dev", "staging", "prod")
MAX_REPLICAS = 50


def validate_replicas(value):
    assert isinstance(value, int) and not isinstance(value, bool), "replicas must be an integer"
    assert 1 <= value <= MAX_REPLICAS, f"replicas must be between 1 and {MAX_REPLICAS}"
    return value


def validate_environment(name):
    assert name in ENVIRONMENTS, f"unknown environment {name!r}"
    return name


def build_manifest(service, replicas, environment):
    return {
        "service": service,
        "replicas": validate_replicas(replicas),
        "environment": validate_environment(environment),
    }


if __name__ == "__main__":
    print(build_manifest("billing", 3, "staging"))
