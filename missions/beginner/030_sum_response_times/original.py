# Mission 030 - Sum the Response Times
# Fix the bug.

def total_ms(times):
    """Return the total of all response times (given as strings)."""
    return sum(times)

if __name__ == "__main__":
    raw = ["120", "340", "89", "456"]
    print(total_ms(raw))
