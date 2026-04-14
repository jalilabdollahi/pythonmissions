# Mission 108 - Solution
def align_name(name, width=20):
    return name.ljust(width)

if __name__ == "__main__":
    for svc in ["web", "api", "database"]:
        print(f"|{align_name(svc, 15)}| status |")
