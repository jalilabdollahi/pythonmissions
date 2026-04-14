# Mission 044 - Number the Steps
# Fix the bug.

def numbered_steps(steps):
    """Return steps numbered starting from 1."""
    return [f"{i}. {step}" for i, step in enumerate(steps)]

if __name__ == "__main__":
    steps = ["Pull image", "Run migrations", "Start service"]
    for s in numbered_steps(steps):
        print(s)
