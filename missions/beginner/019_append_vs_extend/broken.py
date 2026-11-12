# Mission 019 - Nested Host Lists
# Merges per-region host inventories into one flat list.
def merge_regions(regions):
    merged = []
    for region in sorted(regions):
        merged.append(regions[region])
    return merged


def host_count(regions):
    return len(merge_regions(regions))


def patch_targets(regions, suffix):
    return [host for host in merge_regions(regions) if host.endswith(suffix)]


if __name__ == "__main__":
    inv = {"us": ["u1.willow.io", "u2.willow.io"], "eu": ["e1.willow.io"]}
    print(merge_regions(inv), host_count(inv))
