# Mission 046 - Don't Share the Server List
# Fix the bug.

def new_deployment(name, servers=[]):
    """Create a new deployment. servers defaults to empty list."""
    return {"name": name, "servers": servers}

if __name__ == "__main__":
    d1 = new_deployment("prod")
    d1["servers"].append("web-01")
    d2 = new_deployment("staging")
    print(d2["servers"])  # should be empty!
