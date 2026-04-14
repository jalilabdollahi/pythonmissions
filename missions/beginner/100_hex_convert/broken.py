# Mission 100 - Convert the Color Code
def hex_to_int(hex_str):
    """Convert hex color string '#RRGGBB' to integer."""
    return int(hex_str, 16)

if __name__ == "__main__":
    print(hex_to_int("#FF5733"))
