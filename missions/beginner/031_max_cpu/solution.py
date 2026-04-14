# Mission 031 - Solution

def max_cpu(readings):
    return max(readings, default=0)

if __name__ == "__main__":
    print(max_cpu([45.2, 78.9, 92.1, 55.0]))
    print(max_cpu([]))
