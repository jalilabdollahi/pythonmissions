# Mission 016 (Advanced) - NumPy Vectorized Metrics
# Fixed solution
try:
    import numpy as np
except ImportError:
    class np:
        @staticmethod
        def array(x): return x
        @staticmethod
        def mean(x, axis=None):
            if hasattr(x[0], '__iter__') and axis == 1:
                return [sum(row)/len(row) for row in x]
            if hasattr(x[0], '__iter__') and axis == 0:
                return [sum(col)/len(col) for col in zip(*x)]
            return sum(x)/len(x)
        @staticmethod
        def min(x): return min(x) if not hasattr(x[0], '__iter__') else min(min(r) for r in x)
        @staticmethod
        def max(x): return max(x) if not hasattr(x[0], '__iter__') else max(max(r) for r in x)

class MetricsProcessor:
    def per_service_average(self, data):
        arr = np.array(data)
        return np.mean(arr, axis=1)

    def normalize(self, values):
        arr = np.array(values)
        mn = np.min(arr)
        mx = np.max(arr)
        if mx == mn:
            return arr
        return (arr - mn) / (mx - mn)
