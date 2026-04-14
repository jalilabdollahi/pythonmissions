# Mission 127 - Solution
class IPRange:
    def __init__(self, start, count):
        self.base = start
        self.count = count
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.count:
            raise StopIteration
        val = self.base + self.current
        self.current += 1
        return val

if __name__ == "__main__":
    for ip_num in IPRange(1, 3):
        print(f"10.0.0.{ip_num}")
