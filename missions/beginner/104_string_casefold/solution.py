# Mission 104 - Solution
def normalize_user(name):
    return name.casefold()

def same_user(a, b):
    return normalize_user(a) == normalize_user(b)

if __name__ == "__main__":
    print(same_user("Admin", "ADMIN"))
    print(same_user("stra\u00dfe", "STRASSE"))
