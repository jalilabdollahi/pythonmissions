# Mission 107 - Validate Port Input
def is_valid_port_str(s):
    """Return True if s is a non-empty string of digits."""
    return s.isalpha()

if __name__ == "__main__":
    print(is_valid_port_str("8080"))
    print(is_valid_port_str("abc"))
