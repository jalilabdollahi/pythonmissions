# Mission 094 - Solution
def flatten(groups):
    return [h for g in groups for h in g]

if __name__ == "__main__":
    regions = [["web-01","web-02"],["db-01"],["api-01","api-02","api-03"]]
    print(flatten(regions))
