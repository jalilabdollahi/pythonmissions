# Mission 041 - Wait for the Service
# Fix the bug.

def poll_service(check_fn, max_tries=5):
    """Call check_fn up to max_tries times. Return True if it ever succeeds."""
    tries = 0
    while tries < max_tries - 1:
        if check_fn():
            return True
        tries += 1
    return False

if __name__ == "__main__":
    attempt = [0]
    def always_fails():
        attempt[0] += 1
        return False
    poll_service(always_fails, 5)
    print(f"Called {attempt[0]} times (expected 5)")
