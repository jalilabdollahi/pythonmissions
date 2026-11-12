# Mission 201 - Rolling Window Iterator (solution)
# A reusable iterator that yields sliding windows over CPU samples.


class RollingWindows:
    def __init__(self, samples, size):
        if size < 1:
            raise ValueError("size must be at least 1")
        self._samples = list(samples)
        self._size = size
        self._pos = 0

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos + self._size > len(self._samples):
            raise StopIteration
        window = tuple(self._samples[self._pos:self._pos + self._size])
        self._pos += 1
        return window

    def __repr__(self):
        return f"RollingWindows(size={self._size}, samples={len(self._samples)})"

    def __len__(self):
        return max(0, len(self._samples) - self._size + 1)


def sustained_spike(samples, size, limit):
    for window in RollingWindows(samples, size):
        if sum(window) / len(window) >= limit:
            return True
    return False


def peak_window(samples, size):
    return max(RollingWindows(samples, size), key=sum, default=None)


if __name__ == "__main__":
    print(list(RollingWindows([10, 20, 90, 95, 99], 3)))
