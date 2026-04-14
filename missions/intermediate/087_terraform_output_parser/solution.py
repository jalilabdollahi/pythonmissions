# Mission 087 - Terraform Output Parser
# Fixed solution
import json

def parse_tf_output(json_str):
    data = json.loads(json_str)
    result = {}
    for name, meta in data.items():
        result[name] = meta.get("value")
    return result

def get_output_value(json_str, key):
    outputs = parse_tf_output(json_str)
    value = outputs.get(key)
    if value is None:
        return None
    return str(value)
