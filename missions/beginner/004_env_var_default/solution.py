# Mission 004 - Optional Setting Crash (solution)
# Loads worker settings from environment variables with defaults.
import os


def load_settings(env=None):
    env = os.environ if env is None else env
    return {
        "region": env["REGION"],
        "retention_days": env.get("RETENTION_DAYS", "7"),
        "notify_email": env.get("NOTIFY_EMAIL", ""),
    }


def describe(settings):
    parts = [f"region={settings['region']}", f"retention={settings['retention_days']}d"]
    if settings["notify_email"]:
        parts.append(f"notify={settings['notify_email']}")
    return ", ".join(parts)


if __name__ == "__main__":
    print(describe(load_settings()))
