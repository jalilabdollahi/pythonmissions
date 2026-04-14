# Mission 095 - Solution
def classify(code):
    return "ok" if code < 400 else "error"

def batch_classify(codes):
    return [classify(c) for c in codes]

if __name__ == "__main__":
    print(batch_classify([200, 201, 404, 500, 302]))
