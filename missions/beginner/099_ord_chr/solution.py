# Mission 099 - Solution
def next_code(letter):
    return chr(ord(letter) + 1)

if __name__ == "__main__":
    print(next_code("a"))
    print(next_code("z"))
