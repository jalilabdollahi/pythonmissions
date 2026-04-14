# Mission 050 - Config Schema Validator
# Fix the 2 bugs in this script.

SCHEMA = {
    "host": str,
    "port": int,
    "debug": bool,
    "workers": int,
}

def validate_config(config, schema=None):
    schema = schema or SCHEMA
    errors = []
    for key, expected_type in schema.items():
        if key not in config:
            errors.append(f"Missing key: {key}")
            return errors  # BUG 1: returns early, misses other errors
        value = config[key]
        if not isinstance(value, expected_type):
            errors.append(f"{key}: expected {expected_type.__name__}, got {type(value).__name__}")
    return errors

def is_valid(config):
    return validate_config(config) == []
