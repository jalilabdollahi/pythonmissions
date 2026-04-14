# Mission 065 - Solution
def unique_sorted(items):
    return list(sorted(set(items)))

if __name__ == "__main__":
    alerts = ["CRITICAL","WARN","CRITICAL","INFO","WARN"]
    print(unique_sorted(alerts))
