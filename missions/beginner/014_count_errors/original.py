# Mission 014 - Count the Errors
# Fix the bug.

def count_errors(log):
    """Count the number of ERROR entries in a log string."""
    return log.count("error")

if __name__ == "__main__":
    sample = "ERROR: disk full\nINFO: ok\nERROR: OOM\n"
    print(count_errors(sample))
