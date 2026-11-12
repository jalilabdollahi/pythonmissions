# Mission 023 - Biggest CPU Hogs (solution)
# Lists the busiest processes on a node.
def top_cpu(usage, n=3):
    ranked = sorted(usage.items(), key=lambda item: item[1], reverse=True)
    return [name for name, _ in ranked[:n]]


def cpu_report(usage, n=3):
    lines = []
    for position, name in enumerate(top_cpu(usage, n), start=1):
        lines.append(f"{position}. {name} {usage[name]:.1f}%")
    return lines


if __name__ == "__main__":
    sample = {"nginx": 4.0, "batch-export": 97.5, "cron": 0.2, "etl": 55.1}
    print(cpu_report(sample))
