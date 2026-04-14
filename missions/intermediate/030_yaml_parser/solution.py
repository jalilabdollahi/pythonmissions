# Mission 030 - YAML Config Parser
# Fixed solution
import yaml

def parse_manifest(content):
    data = yaml.safe_load(content)
    return data

def get_replicas(manifest_content):
    data = parse_manifest(manifest_content)
    spec = data.get("spec", {})
    return spec.get("replicas", 1)
