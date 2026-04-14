# Mission 073 - Top N Error Codes
from collections import Counter

def top_errors(codes, n=3):
    """Return top n most frequent error codes as (code, count) pairs."""
    return Counter(codes)

if __name__ == "__main__":
    codes = [500, 404, 500, 503, 500, 404, 200, 503, 500]
    print(top_errors(codes, 3))
