# Mission 019 - Solution

def mask_secret(s):
    return "*" * (len(s) - 4) + s[-4:]

if __name__ == "__main__":
    print(mask_secret("mysupersecrettoken"))
