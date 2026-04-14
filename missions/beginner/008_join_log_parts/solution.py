# Mission 008 - Solution

def build_message(parts):
    return " | ".join(parts)

if __name__ == "__main__":
    print(build_message(["ERROR", "web-01", "disk full"]))
