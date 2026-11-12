# Mission 034 - Off-by-One Error Report (solution)
# Report the line number of every ERROR in a log file.


def error_report(lines):
    report = []
    for number, text in enumerate(lines, start=1):
        if "ERROR" in text:
            report.append(f"line {number}: {text.strip()}")
    return report


def format_summary(lines):
    count = len(error_report(lines))
    return f"{count} error(s)"
