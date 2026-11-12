# Mission 197 - Exit Code Map
# Map exceptions to process exit codes for a deployment CLI.
import sys


class DeployError(Exception):
    pass


class ConfigError(DeployError):
    pass


class SchemaError(ConfigError):
    pass


class RolloutTimeout(DeployError):
    pass


EXIT_CODES = [
    (DeployError, 1),
    (ConfigError, 2),
    (SchemaError, 3),
    (RolloutTimeout, 4),
]

UNKNOWN_ERROR = 1


def exit_code_for(exc):
    for cls, code in EXIT_CODES:
        if isinstance(exc, cls):
            return code
    return UNKNOWN_ERROR


def run_cli(action):
    try:
        action()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exit_code_for(exc)
    return 0


if __name__ == "__main__":
    sys.exit(run_cli(lambda: None))
