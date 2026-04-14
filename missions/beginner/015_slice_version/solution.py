# Mission 015 - Solution

def get_major(version):
    dot = version.find(".")
    return version[:dot]

if __name__ == "__main__":
    print(get_major("2.14.3"))
    print(get_major("10.0.1"))
