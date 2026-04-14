# Mission 099 - Increment the Server Code
def next_code(letter):
    """Return the next ASCII letter after letter."""
    return ord(chr(letter) + 1)

if __name__ == "__main__":
    print(next_code("a"))
    print(next_code("z"))
