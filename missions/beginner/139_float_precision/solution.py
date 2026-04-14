# Mission 139 - Solution
def round_metric(value, decimals=2):
    return round(value, decimals)

if __name__ == "__main__":
    print(round_metric(45.6789))
    print(round_metric(99.9999, 1))
