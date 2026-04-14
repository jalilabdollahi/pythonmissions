# Mission 050 - Config Schema Validator
# Fixed solution

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
            continue
        value = config[key]
        if not isinstance(value, expected_type):
            errors.append(f"{key}: expected {expected_type.__name__}, got {type(value).__name__}")
    return errors

def is_valid(config):
    return validate_config(config) == []
