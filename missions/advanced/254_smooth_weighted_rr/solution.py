# Mission 254 - Smooth Weighted Balancer (solution)
# Smooth weighted round-robin (the algorithm nginx uses) with health marking.
from collections import Counter


class NoBackendAvailable(Exception):
    pass


class Backend:
    def __init__(self, name, weight):
        if weight < 0:
            raise ValueError("weight cannot be negative")
        self.name = name
        self.weight = weight
        self.current = 0
        self.up = True

    def __repr__(self):
        state = "up" if self.up else "down"
        return f"Backend({self.name!r}, w={self.weight}, {state})"


class SmoothBalancer:
    def __init__(self, weights):
        self.backends = [Backend(name, weight) for name, weight in weights.items()]
        self.served = Counter()

    def _find(self, name):
        for backend in self.backends:
            if backend.name == name:
                return backend
        raise KeyError(name)

    def _candidates(self):
        return [b for b in self.backends if b.up and b.weight > 0]

    def pick(self):
        candidates = self._candidates()
        if not candidates:
            raise NoBackendAvailable("every backend is down or has zero weight")
        total = sum(b.weight for b in candidates)
        best = None
        for backend in candidates:
            backend.current += backend.weight
            if best is None or backend.current > best.current:
                best = backend
        best.current -= total
        self.served[best.name] += 1
        return best.name

    def mark_down(self, name):
        self._find(name).up = False

    def mark_up(self, name):
        backend = self._find(name)
        backend.up = True
        backend.current = 0

    def set_weight(self, name, weight):
        if weight < 0:
            raise ValueError("weight cannot be negative")
        backend = self._find(name)
        backend.weight = weight
        backend.current = 0

    def add(self, name, weight):
        self.backends.append(Backend(name, weight))

    def remove(self, name):
        self.backends.remove(self._find(name))

    def sequence(self, count):
        return [self.pick() for _ in range(count)]

    def shares(self):
        total = sum(self.served.values()) or 1
        return {name: round(n / total, 3) for name, n in sorted(self.served.items())}
