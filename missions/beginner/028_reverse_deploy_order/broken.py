# Mission 028 - Reverse the Deploy Order
# Fix the bug.

def reversed_order(steps):
    """Return a new list in reversed order."""
    return steps.reverse()

if __name__ == "__main__":
    deploy = ["db-migrate", "backend", "frontend"]
    print(reversed_order(deploy))
