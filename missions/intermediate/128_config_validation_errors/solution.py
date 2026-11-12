# Mission 128 - Collect Every Error (solution)
# Validate a service manifest and report all problems at once.

REQUIRED = ("name", "port", "replicas", "env")


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def check_field(key, value):
    """Return an error message for one present field, or None if it is fine."""
    if key == "name":
        if not isinstance(value, str) or not value.strip():
            return "name must be a non-empty string"
    elif key == "port":
        if not is_int(value) or not 1 <= value <= 65535:
            return "port must be an integer between 1 and 65535"
    elif key == "replicas":
        if not is_int(value) or value < 1:
            return "replicas must be an integer >= 1"
    elif key == "env":
        if not isinstance(value, dict):
            return "env must be a mapping"
    return None


def validate_manifest(cfg):
    errors = []
    for key in REQUIRED:
        if key not in cfg:
            errors.append(f"{key} is missing")
            continue
        problem = check_field(key, cfg[key])
        if problem:
            errors.append(problem)
            
    return errors


def assert_valid(cfg):
    errors = validate_manifest(cfg)
    if errors:
        raise ValueError("; ".join(errors))
