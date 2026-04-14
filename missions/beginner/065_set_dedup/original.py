# Mission 065 - Unique Alert Types
def unique_sorted(items):
    """Return sorted list of unique items."""
    return list(sorted(items))

if __name__ == "__main__":
    alerts = ["CRITICAL","WARN","CRITICAL","INFO","WARN"]
    print(unique_sorted(alerts))
