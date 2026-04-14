# Mission 139 - Round the Metric Value
def round_metric(value, decimals=2):
    """Return value rounded to decimals decimal places."""
    return round(decimals, value)

if __name__ == "__main__":
    print(round_metric(45.6789))
    print(round_metric(99.9999, 1))
