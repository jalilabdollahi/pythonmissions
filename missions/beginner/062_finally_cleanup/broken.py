# Mission 062 - Deploy Lock Stuck On
# Serialises deployments with a simple in-process lock flag.


class Deployer:
    def __init__(self):
        self.locked = False
        self.runs = 0

    def run(self, steps):
        if self.locked:
            raise RuntimeError("deploy already running")
        self.locked = True
        self.runs += 1
        results = []
        for step in steps:
            results.append(step())
        self.locked = False
        return results

    def is_idle(self):
        return not self.locked


def migrate():
    return "migrated"


def restart():
    return "restarted"


if __name__ == "__main__":
    print(Deployer().run([migrate, restart]))
