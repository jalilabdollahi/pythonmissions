# Mission 044 - Solution

def numbered_steps(steps):
    return [f"{i}. {step}" for i, step in enumerate(steps, 1)]

if __name__ == "__main__":
    steps = ["Pull image", "Run migrations", "Start service"]
    for s in numbered_steps(steps):
        print(s)
