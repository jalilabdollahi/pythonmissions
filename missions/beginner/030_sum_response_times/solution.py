# Mission 030 - Solution

def total_ms(times):
    return sum(int(t) for t in times)

if __name__ == "__main__":
    raw = ["120", "340", "89", "456"]
    print(total_ms(raw))
