# Mission 089 - Jobs Leaking Between Servers (solution)
# Simple batch scheduler with per-server job queues.


class Server:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.jobs = []

    def has_room(self):
        return len(self.jobs) < self.capacity

    def assign(self, job):
        if not self.has_room():
            return False
        self.jobs.append(job)
        return True

    def load(self):
        return len(self.jobs)


def least_loaded(servers):
    return min(servers, key=lambda s: s.load())


def dispatch(servers, jobs):
    placed = {}
    for job in jobs:
        target = least_loaded(servers)
        if target.assign(job):
            placed[job] = target.name
    return placed


if __name__ == "__main__":
    pool = [Server("node-a", 2), Server("node-b", 2)]
    print(dispatch(pool, ["etl", "report", "export"]))
