# Mission 100 - Solution
def hex_to_int(hex_str):
    return int(hex_str.lstrip("#"), 16)

if __name__ == "__main__":
    print(hex_to_int("#FF5733"))
