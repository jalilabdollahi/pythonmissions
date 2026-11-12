# Mission 217 - JUnit Result Digest (solution)
# Summarise JUnit XML test reports for a chat digest.
import xml.etree.ElementTree as ET


def summarize(xml_text):
    root = ET.fromstring(xml_text)
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    failures = []
    for case in root.iter("testcase"):
        name = f"{case.get('classname')}.{case.get('name')}"
        if case.find("failure") is not None:
            counts["failed"] += 1
            failures.append(name)
        elif case.find("error") is not None:
            counts["errors"] += 1
            failures.append(name)
        elif case.find("skipped") is not None:
            counts["skipped"] += 1
        else:
            counts["passed"] += 1
    counts["failures"] = sorted(failures)
    return counts


def total_time(xml_text):
    root = ET.fromstring(xml_text)
    return round(sum(float(case.get("time", 0)) for case in root.iter("testcase")), 3)


def is_green(summary):
    return summary["failed"] == 0 and summary["errors"] == 0


def digest(summary):
    total = summary["passed"] + summary["failed"] + summary["errors"] + summary["skipped"]
    state = "GREEN" if is_green(summary) else "RED"
    return (
        f"{state}: {summary['passed']}/{total} passed, {summary['failed']} failed, "
        f"{summary['errors']} errors, {summary['skipped']} skipped"
    )


if __name__ == "__main__":
    print(digest(summarize("<testsuite><testcase classname='a' name='b'/></testsuite>")))
