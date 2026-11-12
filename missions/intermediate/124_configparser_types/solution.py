# Mission 124 - Typed INI Settings (solution)
# Load worker tuning options from an INI file with typed values and defaults.
import configparser


def load_settings(path):
    cp = configparser.ConfigParser()
    cp.read(path)
    return {
        "threads": cp.getint("worker", "threads", fallback=4),
        "debug": cp.getboolean("worker", "debug", fallback=False),
        "timeout": cp.getfloat("worker", "timeout", fallback=30.0),
    }


def describe(settings):
    mode = "debug" if settings["debug"] else "quiet"
    return f"{settings['threads']} threads, {mode}, timeout {settings['timeout']}s"
