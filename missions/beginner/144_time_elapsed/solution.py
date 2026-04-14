# Mission 144 - Solution
import time

def elapsed_seconds(start):
    return time.time() - start

if __name__ == "__main__":
    import time
    t = time.time()
    import time as _time
    _time.sleep(0.1)
    print(f"Elapsed: {elapsed_seconds(t):.3f}s")
