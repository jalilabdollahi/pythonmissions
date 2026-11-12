# Mission 015 - PROD Is Not prod (solution)
# Counts production instances from messy environment tags.
PRODUCTION_NAMES = {"prod", "production"}


def normalize(tag):
    if not tag:
        return "untagged"
    return tag.strip().lower()


def is_production(tag):
    return bool(tag) and tag.strip().lower() in PRODUCTION_NAMES


def count_production(instances):
    return sum(1 for item in instances if is_production(item.get("environment")))


def by_environment(instances):
    counts = {}
    for item in instances:
        key = normalize(item.get("environment"))
        counts[key] = counts.get(key, 0) + 1
    return counts


if __name__ == "__main__":
    print(count_production([{"environment": "PROD"}, {"environment": "qa"}]))
