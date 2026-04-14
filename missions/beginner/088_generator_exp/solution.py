# Mission 088 - Solution
def metric_lines(metrics):
    return (f"{k}={v}" for k, v in metrics.items())

if __name__ == "__main__":
    import types
    m = {"cpu": 45, "mem": 78, "disk": 60}
    gen = metric_lines(m)
    print(type(gen))
    for line in gen:
        print(line)
