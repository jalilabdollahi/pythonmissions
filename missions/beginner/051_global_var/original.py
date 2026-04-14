# Mission 051 - Fix the Global Counter
COUNTER = 0

def increment_counter():
    """Add 1 to the global COUNTER."""
    COUNTER = COUNTER + 1

def get_counter():
    return COUNTER

if __name__ == "__main__":
    increment_counter()
    increment_counter()
    print(get_counter())
