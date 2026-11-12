# Mission 202 - Triage Queue Order
# Order incidents for the on-call engineer using stable multi-pass sorting.

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def severity_key(incident):
    return incident["severity"]


def triage_order(incidents):
    ordered = incidents
    ordered.sort(key=lambda inc: inc["id"])
    ordered.sort(key=severity_key)
    ordered.sort(key=lambda inc: inc["opened"])
    return ordered


def oncall_page_list(incidents, limit=3):
    return [inc["id"] for inc in triage_order(incidents)[:limit]]


def group_by_team(incidents):
    teams = {}
    for inc in triage_order(incidents):
        teams.setdefault(inc["team"], []).append(inc["id"])
    return teams


def worst_severity(incidents):
    if not incidents:
        return None
    return triage_order(incidents)[0]["severity"]


def severity_counts(incidents):
    counts = {}
    for inc in incidents:
        counts[inc["severity"]] = counts.get(inc["severity"], 0) + 1
    return dict(sorted(counts.items(), key=lambda item: SEVERITY_RANK[item[0]]))


if __name__ == "__main__":
    demo = [{"id": "INC-2", "severity": "low", "opened": "2024-05-01T08:00", "team": "db"}]
    print(oncall_page_list(demo))
