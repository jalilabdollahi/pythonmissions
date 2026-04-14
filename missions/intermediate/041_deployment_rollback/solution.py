# Mission 041 - Deployment Rollback
# Fixed solution

class DeploymentStack:
    def __init__(self):
        self.versions = []

    def deploy(self, version):
        self.versions.append(version)
        return f"Deployed {version}"

    def rollback(self):
        if len(self.versions) < 2:
            raise RuntimeError("Nothing to roll back to")
        return self.versions.pop()

    def can_rollback(self):
        return len(self.versions) > 1

    def current(self):
        return self.versions[-1] if self.versions else None
