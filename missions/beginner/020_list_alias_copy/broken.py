# Mission 020 - The Shared Allow-List
# Builds per-customer proxy configs from shared defaults.
DEFAULT_ALLOWED = ["10.0.0.0/8", "192.168.0.0/16"]


def build_config(customer, extra_ranges=()):
    allowed = DEFAULT_ALLOWED
    for cidr in extra_ranges:
        allowed.append(cidr)
    return {"customer": customer, "allowed": allowed}


def allowed_count(config):
    return len(config["allowed"])


if __name__ == "__main__":
    print(build_config("acme", ["172.16.0.0/12"]))
    print(build_config("globex"))
