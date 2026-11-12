# Mission 071 - Kebab Case Or Bust
# Normalises service names to lower-case kebab-case.


def normalize(name):
    return name.strip().capitalize().replace(" ", "-")


def normalize_all(names):
    return [normalize(name) for name in names]


def conflicts(names):
    seen = {}
    for name in normalize_all(names):
        seen[name] = seen.get(name, 0) + 1
    return sorted(name for name, count in seen.items() if count > 1)


def is_normalized(name):
    return name == normalize(name)


def registry_key(team, name):
    return "%s/%s" % (normalize(team), normalize(name))


if __name__ == "__main__":
    print(normalize_all(["Payment Gateway", "Auth_Service"]))
