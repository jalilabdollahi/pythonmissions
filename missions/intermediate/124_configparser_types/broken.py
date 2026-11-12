# Mission 124 - Typed INI Settings
# Load worker tuning options from an INI file with typed values and defaults.
import configparser


def load_settings(path):
    cp = configparser.ConfigParser()
    cp.read(path)
    return {
        "threads": cp.get("worker", "threads", fallback=4),
        "debug": bool(cp.get("worker", "debug", fallback="no")),
        "timeout": cp["worker"].getfloat("timeout", 30.0),
    }


def describe(settings):
    mode = "debug" if settings["debug"] else "quiet"
    return f"{settings['threads']} threads, {mode}, timeout {settings['timeout']}s"
