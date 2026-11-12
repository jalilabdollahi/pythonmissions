# Mission 058 - Noisy Config Diffs
# Renders configuration data as stable JSON text for git.
import json


def render_manifest(data):
    return json.dumps(data, indent=2)


def render_snapshot(data):
    return json.dumps(data, sort_keys=True)


def write_snapshot(path, data):
    text = render_snapshot(data) + "\n"
    with open(path, "w") as handle:
        handle.write(text)
    return len(text)


def has_changed(old, new):
    return render_manifest(old) != render_manifest(new)


def line_count(data):
    return len(render_snapshot(data).splitlines())


if __name__ == "__main__":
    print(render_manifest({"b": 1, "a": {"y": 2, "x": 3}}))
