# Mission 022 - Build 10 Before Build 9
# Orders CI build numbers that arrive as text.
def ordered_builds(builds):
    return sorted(builds)


def latest_build(builds):
    ordered = ordered_builds(builds)
    return ordered[-1] if ordered else None


def builds_after(builds, last_deployed):
    cutoff = int(last_deployed)
    return [b for b in ordered_builds(builds) if int(b) > cutoff]


if __name__ == "__main__":
    print(latest_build(["98", "99", "100"]))
