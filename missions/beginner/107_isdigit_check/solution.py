# Mission 107 - Solution
def is_valid_port_str(s):
    return s.isdigit()

if __name__ == "__main__":
    print(is_valid_port_str("8080"))
    print(is_valid_port_str("abc"))
