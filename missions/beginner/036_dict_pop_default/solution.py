# Mission 036 - Solution

def remove_flag(flags, name):
    return flags.pop(name, False)

if __name__ == "__main__":
    flags = {"dark_mode": True, "beta_api": False}
    print(remove_flag(flags, "dark_mode"))
    print(remove_flag(flags, "nonexistent"))
