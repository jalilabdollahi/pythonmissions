# Mission 116 - Solution
import heapq

def slowest_three(times):
    return heapq.nlargest(3, times)

if __name__ == "__main__":
    times = [120, 340, 89, 2000, 456, 1500, 78, 900]
    print(slowest_three(times))
