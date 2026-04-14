# Mission 030 - YAML Config Parser
# Fix the 2 bugs in this script.
import yaml

def parse_manifest(content):
    data = yaml.load(content)  # BUG 1: insecure, should be yaml.safe_load()
    return data

def get_replicas(manifest_content):
    data = parse_manifest(manifest_content)
    spec = data["spec"]  # BUG 2: should use .get() to avoid KeyError
    return spec.get("replicas", 1)
