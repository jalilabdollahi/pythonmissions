# Mission 060 - Half A Core Of Trouble (solution)
# Parses CPU percentage readings reported by a metrics agent.


def parse_cpu(text):
    cleaned = text.strip().rstrip("%").strip()
    return float(cleaned)


def hottest(readings):
    parsed = {pod: parse_cpu(value) for pod, value in readings.items()}
    return max(parsed, key=parsed.get)


def average_cpu(readings):
    values = [parse_cpu(value) for value in readings.values()]
    return sum(values) / len(values)


def needs_scale_up(readings, limit=75.0):
    return average_cpu(readings) > limit


def describe(readings):
    return "avg %.1f%%, hottest %s" % (average_cpu(readings), hottest(readings))


if __name__ == "__main__":
    print(describe({"web-1": "12.5%", "web-2": "80%"}))
