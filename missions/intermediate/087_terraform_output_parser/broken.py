# Mission 087 - Terraform Output Parser
# Fix the 2 bugs in this script.
import json

def parse_tf_output(json_str):
    """Parse terraform output -json and return flat {name: value} dict."""
    data = json.loads(json_str)
    result = {}
    for name, meta in data.items():
        result[name] = meta  # BUG 1: should extract meta["value"]
    return result

def get_output_value(json_str, key):
    outputs = parse_tf_output(json_str)
    value = outputs.get(key)
    if value is None:
        return None
    return str(value).upper()  # BUG 2: .upper() will fail on non-string types like int/list
