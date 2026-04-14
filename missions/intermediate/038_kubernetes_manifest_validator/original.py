# Mission 038 - K8s Manifest Validator
# Fix the 2 bugs in this script.

REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec"]

def validate_deployment(manifest):
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    # Check replicas is an integer
    spec = manifest.get("spec", {})
    replicas = spec.get("replicas", 1)
    if type(replicas) == str:  # BUG 1: should use isinstance(replicas, int) for proper type check
        errors.append("replicas must be an integer")

    # Check metadata has name
    metadata = manifest.get("metadata", {})
    if "names" in metadata:  # BUG 2: key is "name" not "names"
        errors.append("metadata.name is required")

    return errors
