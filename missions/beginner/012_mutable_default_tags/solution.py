# Mission 012 - Tags That Follow You (solution)
# Builds tag lists for cloud resources.
def tag_resource(name, tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def standard_tags(owner):
    tags = tag_resource("bucket", f"owner:{owner}")
    return tag_resource("bucket", "managed:true", tags)


if __name__ == "__main__":
    print(standard_tags("payments"))
    print(standard_tags("risk"))
