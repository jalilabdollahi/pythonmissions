# Mission 015 - Slice the Version
# Fix the bug.

def get_major(version):
    """Return the major version number as a string."""
    dot = version.find(".")
    return version[1:dot]

if __name__ == "__main__":
    print(get_major("2.14.3"))
    print(get_major("10.0.1"))
