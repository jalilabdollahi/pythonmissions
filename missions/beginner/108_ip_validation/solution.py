# Mission 108 - Allow-List Sanitiser (solution)
# Validates IP addresses coming from a user-supplied allow-list.
import ipaddress


def is_valid_ip(text):
    try:
        ipaddress.ip_address(text.strip())
    except ValueError:
        return False
    return True


def ip_family(text):
    if not is_valid_ip(text):
        return None
    return ipaddress.ip_address(text.strip()).version


def split_valid(candidates):
    good = []
    bad = []
    for entry in candidates:
        if is_valid_ip(entry):
            good.append(entry.strip())
        else:
            bad.append(entry)
    return good, bad


def summarize(candidates):
    good, bad = split_valid(candidates)
    return f"{len(good)} accepted, {len(bad)} rejected"


if __name__ == "__main__":
    print(summarize(["10.0.0.1", "2001:db8::1", "oops"]))
