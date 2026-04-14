# Mission 006 - Strip the Noise
# Fix the bug in this script.

def clean_name(s):
    """Remove leading and trailing whitespace from a server name."""
    return s.lstrip()

def batch_clean(names):
    return [clean_name(n) for n in names]

if __name__ == "__main__":
    print(clean_name("  prod-web-01  \n"))
