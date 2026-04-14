# Mission 031 - Find the Max CPU
# Fix the bug.

def max_cpu(readings):
    """Return the highest CPU reading, or 0 if no readings."""
    return max(readings)

if __name__ == "__main__":
    print(max_cpu([45.2, 78.9, 92.1, 55.0]))
    print(max_cpu([]))
