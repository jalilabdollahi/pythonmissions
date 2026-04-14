# Mission 108 - Align the Report Table
def align_name(name, width=20):
    """Return name left-justified in a field of width chars."""
    return name.rjust(width)

if __name__ == "__main__":
    for svc in ["web", "api", "database"]:
        print(f"|{align_name(svc, 15)}| status |")
