# Mission 081 - Stopped Containers Cleanup (solution)
# Builds a safe removal plan for dead containers on a CI host.


def running_names(containers):
    return [c["name"] for c in containers if c["state"] == "running"]


def stopped_names(containers):
    return [c["name"] for c in containers if c["state"] != "running"]


def removable(containers, min_age_hours):
    return [
        c["name"]
        for c in containers
        if c["state"] != "running" and c["age_hours"] >= min_age_hours
    ]


def cleanup_plan(containers, min_age_hours):
    return [f"docker rm {name}" for name in removable(containers, min_age_hours)]


def describe(containers):
    live = len(running_names(containers))
    dead = len(stopped_names(containers))
    return f"{live} running, {dead} stopped"


if __name__ == "__main__":
    fleet = [
        {"name": "web", "state": "running", "age_hours": 3},
        {"name": "job-41", "state": "exited", "age_hours": 30},
        {"name": "job-42", "state": "created", "age_hours": 1},
    ]
    print(describe(fleet))
    for cmd in cleanup_plan(fleet, 24):
        print(cmd)
