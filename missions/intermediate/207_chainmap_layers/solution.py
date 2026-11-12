# Mission 207 - Layered Settings (solution)
# Layer worker settings with ChainMap: cli > env > file > defaults.
from collections import ChainMap


def resolve(defaults, file_cfg, env, cli):
    cli_given = {key: value for key, value in cli.items() if value is not None}
    return ChainMap(cli_given, env, file_cfg, defaults)


def effective(settings):
    return dict(settings)


def worker_count(settings):
    return int(settings["workers"])


def debug_enabled(settings):
    value = settings.get("debug", False)
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def missing_required(settings, required):
    return sorted(key for key in required if key not in settings)


def describe_sources(settings, names=("cli", "env", "file", "defaults")):
    sources = {}
    for key in effective(settings):
        for name, layer in zip(names, settings.maps):
            if key in layer:
                sources[key] = name
                break
    return sources


if __name__ == "__main__":
    cfg = resolve({"workers": 2}, {"workers": 4}, {"workers": "6"}, {"workers": 8})
    print(worker_count(cfg), describe_sources(cfg))
