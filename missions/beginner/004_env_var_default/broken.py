# Mission 004 - Optional Setting Crash
# Loads worker settings from environment variables with defaults.
import os


def load_settings(env=None):
    env = os.environ if env is None else env
    return {
        "region": env["REGION"],
        "retention_days": env["RETENTION_DAYS"],
        "notify_email": env["NOTIFY_EMAIL"],
    }


def describe(settings):
    parts = [f"region={settings['region']}", f"retention={settings['retention_days']}d"]
    if settings["notify_email"]:
        parts.append(f"notify={settings['notify_email']}")
    return ", ".join(parts)


if __name__ == "__main__":
    print(describe(load_settings()))
