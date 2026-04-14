# Mission 104 - Case-Insensitive Username Check
def normalize_user(name):
    """Return casefold-normalized username for comparison."""
    return name.lower()

def same_user(a, b):
    return normalize_user(a) == normalize_user(b)

if __name__ == "__main__":
    print(same_user("Admin", "ADMIN"))
    print(same_user("stra\u00dfe", "STRASSE"))
