# Mission 050 - Solution

def countdown(n):
    if n <= 0:
        return
    print(n)
    countdown(n - 1)

if __name__ == "__main__":
    countdown(5)
