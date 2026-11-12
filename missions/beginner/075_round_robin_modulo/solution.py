# Mission 075 - Round Robin Roulette (solution)
# A minimal round-robin picker for a pool of encoder backends.


class RoundRobin:
    def __init__(self, backends):
        if not backends:
            raise ValueError("no backends")
        self.backends = list(backends)
        self.counter = 0
        self.served = 0

    def next_backend(self):
        index = self.counter % len(self.backends)
        self.counter += 1
        self.served += 1
        return self.backends[index]

    def peek_cycle(self, count):
        return [self.next_backend() for _ in range(count)]

    def reset(self):
        self.counter = 0

    def share(self, backend):
        if self.served == 0:
            return 0.0
        return self.peek_count(backend) / self.served

    def peek_count(self, backend):
        full, rest = divmod(self.served, len(self.backends))
        position = self.backends.index(backend)
        return full + (1 if position < rest else 0)


if __name__ == "__main__":
    print(RoundRobin(["enc-1", "enc-2", "enc-3"]).peek_cycle(6))
