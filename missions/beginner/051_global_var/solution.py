# Mission 051 - Solution
COUNTER = 0

def increment_counter():
    global COUNTER
    COUNTER = COUNTER + 1

def get_counter():
    return COUNTER

if __name__ == "__main__":
    increment_counter()
    increment_counter()
    print(get_counter())
