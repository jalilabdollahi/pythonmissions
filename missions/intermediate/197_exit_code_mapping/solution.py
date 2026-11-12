# Mission 197 - Exit Code Map (solution)
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
    (SchemaError, 3),
    (ConfigError, 2),
    (RolloutTimeout, 4),
    (DeployError, 1),
]

UNKNOWN_ERROR = 70


def exit_code_for(exc):
    for cls, code in EXIT_CODES:
        if isinstance(exc, cls):
            return code
    return UNKNOWN_ERROR


def run_cli(action):
    try:
        action()
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return exit_code_for(exc)
    return 0


if __name__ == "__main__":
    sys.exit(run_cli(lambda: None))
