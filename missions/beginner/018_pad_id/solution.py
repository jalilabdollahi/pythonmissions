# Mission 018 - Solution

def pad_id(n):
    return str(n).zfill(6)

if __name__ == "__main__":
    print(pad_id(42))
    print(pad_id(999999))
