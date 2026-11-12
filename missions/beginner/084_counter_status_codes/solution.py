# Mission 084 - Top Status Codes (solution)
# Daily digest of the most common HTTP status codes.
from collections import Counter


def tally(codes):
    return Counter(codes)


def top_codes(codes, n):
    return tally(codes).most_common(n)


def error_share(codes):
    if not codes:
        return 0.0
    errors = sum(1 for c in codes if c >= 400)
    return errors / len(codes)


def digest_line(codes, n):
    return " ".join(f"{code}:{count}" for code, count in top_codes(codes, n))


if __name__ == "__main__":
    sample = [200, 200, 404, 200, 500, 404, 200, 301]
    print(digest_line(sample, 3))
    print(f"{error_share(sample):.0%} errors")
