# Mission 014 - Solution

def count_errors(log):
    return log.count("ERROR")

if __name__ == "__main__":
    sample = "ERROR: disk full\nINFO: ok\nERROR: OOM\n"
    print(count_errors(sample))
