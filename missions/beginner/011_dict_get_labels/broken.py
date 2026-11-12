# Mission 011 - Unlabeled Pods
# Groups pods by their team label for cost reports.
def team_of(pod):
    return pod["labels"]["team"]


def count_by_team(pods):
    counts = {}
    for pod in pods:
        team = team_of(pod)
        counts[team] = counts.get(team, 0) + 1
    return counts


def unowned_pods(pods):
    return [pod["name"] for pod in pods if team_of(pod) == "unowned"]


if __name__ == "__main__":
    demo = [{"name": "cart-1", "labels": {"team": "checkout"}}, {"name": "tmp-9", "labels": {}}]
    print(count_by_team(demo))
