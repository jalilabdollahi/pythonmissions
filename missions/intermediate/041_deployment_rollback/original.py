# Mission 041 - Deployment Rollback
# Fix the 2 bugs in this script.

class DeploymentStack:
    def __init__(self):
        self.versions = []

    def deploy(self, version):
        self.versions.append(version)
        return f"Deployed {version}"

    def rollback(self):
        if not self.versions:
            raise RuntimeError("Nothing to roll back")
        return self.versions.pop(0)  # BUG 1: should pop(-1) or pop() from end

    def can_rollback(self):
        return len(self.versions) > 0  # BUG 2: need at least 2 to roll back

    def current(self):
        return self.versions[-1] if self.versions else None
