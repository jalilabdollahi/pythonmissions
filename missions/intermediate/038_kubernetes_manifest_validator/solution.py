# Mission 038 - K8s Manifest Validator
# Fixed solution

REQUIRED_FIELDS = ["apiVersion", "kind", "metadata", "spec"]

def validate_deployment(manifest):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    spec = manifest.get("spec", {})
    replicas = spec.get("replicas", 1)
    if not isinstance(replicas, int):
        errors.append("replicas must be an integer")

    metadata = manifest.get("metadata", {})
    if "name" not in metadata:
        errors.append("metadata.name is required")

    return errors
