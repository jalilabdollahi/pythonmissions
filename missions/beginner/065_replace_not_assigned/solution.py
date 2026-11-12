# Mission 065 - Hostnames That Never Changed (solution)
# Cleans server inventory names so DNS will accept them.


def sanitize_hostname(name):
    name = name.strip().lower()
    name = name.replace("_", "-")
    name = name.replace(" ", "")
    return name


def fqdn(name, zone):
    return "%s.%s" % (sanitize_hostname(name), zone)


def sanitize_all(names):
    seen = []
    for name in names:
        clean = sanitize_hostname(name)
        if clean not in seen:
            seen.append(clean)
    return seen


def is_valid_label(label):
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    return bool(label) and all(ch in allowed for ch in label)


def invalid_names(names):
    return [n for n in names if not is_valid_label(sanitize_hostname(n))]


if __name__ == "__main__":
    print(fqdn("Web_Server 01", "corp.example"))
