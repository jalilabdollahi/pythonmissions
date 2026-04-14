# Mission 094 - Flatten the Nested Host Lists
def flatten(groups):
    """Flatten list of lists into one list."""
    return [g for g in groups]

if __name__ == "__main__":
    regions = [["web-01","web-02"],["db-01"],["api-01","api-02","api-03"]]
    print(flatten(regions))
