# Mission 006 - Solution

def clean_name(s):
    return s.strip()

def batch_clean(names):
    return [clean_name(n) for n in names]

if __name__ == "__main__":
    print(clean_name("  prod-web-01  \n"))
