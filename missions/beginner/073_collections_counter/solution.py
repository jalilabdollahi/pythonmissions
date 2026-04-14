# Mission 073 - Solution
from collections import Counter

def top_errors(codes, n=3):
    return Counter(codes).most_common(n)

if __name__ == "__main__":
    codes = [500, 404, 500, 503, 500, 404, 200, 503, 500]
    print(top_errors(codes, 3))
