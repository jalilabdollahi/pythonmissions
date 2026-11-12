# Mission 063 - Config Errors Nobody Can Catch
# Validates service configs before a rollout.

REQUIRED_KEYS = ("name", "port", "owner")


class ConfigError:
    pass


def validate_config(cfg):
    for key in REQUIRED_KEYS:
        if key not in cfg:
            raise ConfigError("missing required key")
    return True


def is_valid(cfg):
    try:
        return validate_config(cfg)
    except ConfigError:
        return False


def missing_keys(cfg):
    return [key for key in REQUIRED_KEYS if key not in cfg]


def rollout_ready(configs):
    return [cfg["name"] for cfg in configs if is_valid(cfg)]


if __name__ == "__main__":
    print(is_valid({"name": "web", "port": 80, "owner": "team-a"}))
