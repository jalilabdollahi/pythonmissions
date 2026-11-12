# Mission 175 - Dotted Path Digger (solution)
# Look up values in nested manifests with dotted paths like spec.containers.0.image.
_MISSING = object()


def _step(node, key):
    if isinstance(node, dict):
        return node.get(key, _MISSING)
    if isinstance(node, list):
        try:
            idx = int(key)
        except ValueError:
            return _MISSING
        if -len(node) <= idx < len(node):
            return node[idx]
    return _MISSING


def deep_get(obj, path, default=None):
    node = obj
    for key in path.split("."):
        node = _step(node, key)
        if node is _MISSING:
            return default
    return node


def container_images(pod):
    containers = deep_get(pod, "spec.containers", [])
    images = []
    for i in range(len(containers)):
        image = deep_get(pod, "spec.containers.%d.image" % i)
        if image is not None:
            images.append(image)
    return images


def main():
    pod = {"spec": {"replicas": 0, "containers": [{"image": "web:1"}, {"image": "log:2"}]}}
    print("replicas:", deep_get(pod, "spec.replicas", "unset"))
    print("first image:", deep_get(pod, "spec.containers.0.image"))
    print("images:", container_images(pod))


if __name__ == "__main__":
    main()
