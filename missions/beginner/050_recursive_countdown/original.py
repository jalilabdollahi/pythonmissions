# Mission 050 - Countdown to Deploy
# Fix the bug.

def countdown(n):
    """Print countdown from n to 1 recursively."""
    print(n)
    countdown(n - 1)

if __name__ == "__main__":
    countdown(5)
