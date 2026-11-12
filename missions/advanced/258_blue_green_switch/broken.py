# Mission 258 - Blue/Green Cutover
# Router that deploys to the idle color, gates the switch on health and can roll back.
from collections import namedtuple

CutoverResult = namedtuple("CutoverResult", ["status", "active", "checks"])


class NothingToRollBack(Exception):
    pass


class Slot:
    def __init__(self, version):
        self.version = version


class BlueGreenRouter:
    def __init__(self, initial_version):
        self.slots = {"blue": Slot(initial_version), "green": Slot(None)}
        self.active = "blue"
        self.previous = None
        self.history = []

    @property
    def idle(self):
        return "green" if self.active == "blue" else "blue"

    def deploy(self, version):
        """Install a new version on the idle color; live traffic is untouched."""
        target = self.active
        self.slots[target].version = version
        self.history.append(("deploy", target, version))
        return target

    def live_version(self):
        return self.slots[self.active].version

    def cutover(self, check, required=3, max_checks=6, verify=None):
        target = self.idle
        if self.slots[target].version is None:
            raise ValueError("nothing has been deployed to the idle color")
        passes = 0
        checks = 0
        while checks < max_checks and passes < required:
            checks += 1
            if check(target):
                passes += 1
        if passes < required:
            self.history.append(("blocked", target, None))
            return CutoverResult("blocked", self.active, checks)
        self.previous = self.active
        self.active = target
        self.history.append(("switch", target, self.slots[target].version))
        if verify is not None and not verify(target):
            self.history.append(("auto-rollback", self.active, None))
            return CutoverResult("rolled_back", self.active, checks)
        return CutoverResult("switched", self.active, checks)

    def rollback(self):
        """Send traffic back to the color that served before the last cutover."""
        if self.previous is None:
            raise NothingToRollBack("no previous color to return to")
        self.active, self.previous = self.previous, self.active
        self.history.append(("rollback", self.active, None))
        return self.active

    def status(self):
        return {
            "active": self.active,
            "live_version": self.live_version(),
            "idle_version": self.slots[self.idle].version,
            "can_rollback": self.previous is not None,
        }
