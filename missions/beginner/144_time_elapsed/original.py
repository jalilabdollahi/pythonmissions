# Mission 144 - Measure Deploy Duration
import time

def elapsed_seconds(start):
    """Return seconds elapsed since start timestamp."""
    return time.time()

if __name__ == "__main__":
    import time
    t = time.time()
    time.sleep(0.1)
    print(f"Elapsed: {elapsed_seconds(t):.3f}s")
