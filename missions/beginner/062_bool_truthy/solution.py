# Mission 062 - Solution
def is_enabled(val):
    return val.lower() == "true"

if __name__ == "__main__":
    print(is_enabled("true"))
    print(is_enabled("false"))
    print(is_enabled(""))
