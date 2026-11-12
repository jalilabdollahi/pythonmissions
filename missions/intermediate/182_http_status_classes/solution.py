# Mission 182 - Status Code Sorter (solution)
# Classify HTTP status codes from edge logs and compute error shares.
def classify(code):
    code = int(code)
    if 100 <= code < 200:
        return "informational"
    if 200 <= code < 300:
        return "success"
    if 300 <= code < 400:
        return "redirect"
    if 400 <= code < 500:
        return "client_error"
    if 500 <= code < 600:
        return "server_error"
    return "unknown"


def summarize(codes):
    counts = {}
    for code in codes:
        kind = classify(code)
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def error_rate(codes):
    codes = list(codes)
    if not codes:
        return 0.0
    errors = sum(1 for c in codes if classify(c) == "server_error")
    return errors / len(codes)


def is_retryable(code):
    code = int(code)
    if code in (408, 429):
        return True
    return classify(code) == "server_error" and code not in (501, 505)
