# Mission 047 - Sum Any Number of Metrics
# Fix the bug.

def total(values):
    """Return the sum of any number of metric values."""
    return sum(values)

if __name__ == "__main__":
    print(total(10, 20, 30))
    print(total(5))
