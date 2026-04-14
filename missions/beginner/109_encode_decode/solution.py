# Mission 109 - Solution
def to_bytes(text):
    return text.encode("utf-8")

def to_string(data):
    return data.decode("utf-8")

if __name__ == "__main__":
    b = to_bytes("hello server")
    print(to_string(b))
