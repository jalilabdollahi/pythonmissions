# Mission 138 - Solution
import sys

def print_progress(step, total):
    pct = int(step / total * 100)
    print(f"\rProgress: {pct}%", end="", flush=True)

if __name__ == "__main__":
    import time
    for i in range(1, 6):
        print_progress(i, 5)
        time.sleep(0.1)
    print()
