# Mission 061 - The Except That Ate Everything
# Loads operator settings with forgiving integer parsing.

DEFAULT_REGION = "eu-west"


def parse_retries(value, default=3):
    try:
        return int(value)
    except:
        return default


def load_settings(raw):
    return {
        "retries": parse_retries(raw["retries"]),
        "region": raw.get("region", DEFAULT_REGION),
    }


def effective_attempts(raw):
    settings = load_settings(raw)
    return settings["retries"] + 1


def describe(raw):
    settings = load_settings(raw)
    return "region=%s retries=%d" % (settings["region"], settings["retries"])


if __name__ == "__main__":
    print(describe({"retries": "5"}))
