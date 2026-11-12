# Mission 297 - Release Train States (solution)
# Deployment lifecycle as an explicit state machine with a transition table.

TRANSITIONS = {
    "queued": {"deploying", "cancelled"},
    "deploying": {"verifying", "failed", "cancelled"},
    "verifying": {"live", "failed"},
    "live": {"superseded", "rolling_back"},
    "failed": {"rolling_back"},
    "rolling_back": {"rolled_back", "rollback_failed"},
    "rolled_back": set(),
    "rollback_failed": set(),
    "superseded": set(),
    "cancelled": set(),
}

EVENTS = {
    "start": "deploying",
    "deployed": "verifying",
    "verified": "live",
    "error": "failed",
    "rollback": "rolling_back",
    "rollback_done": "rolled_back",
    "rollback_error": "rollback_failed",
    "replace": "superseded",
    "cancel": "cancelled",
}


class IllegalTransition(Exception):
    pass


class Deployment:
    def __init__(self, deploy_id, clock):
        self.deploy_id = deploy_id
        self.clock = clock
        self.state = "queued"
        self.history = [("queued", clock())]

    def can_move(self, new_state):
        return new_state in TRANSITIONS[self.state]

    def is_terminal(self):
        return not TRANSITIONS[self.state]

    def move(self, new_state):
        """Change state. Returns True if it changed, False for a repeated (duplicate) event."""
        if new_state not in TRANSITIONS:
            raise ValueError(f"unknown state {new_state!r}")
        if new_state == self.state:
            return False
        previous = self.state
        if not self.can_move(new_state):
            raise IllegalTransition(f"{self.deploy_id}: {previous} -> {new_state} is not allowed")
        self.state = new_state
        self.history.append((new_state, self.clock()))
        return True

    def apply(self, event):
        return self.move(EVENTS[event])

    def path(self):
        return [state for state, _ in self.history]


def reachable(start):
    """Every state that can eventually be reached from `start`."""
    seen, todo = set(), [start]
    while todo:
        for nxt in TRANSITIONS[todo.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return seen


def in_flight(deployments):
    """Deployments that still need attention (not in a terminal state)."""
    return [d.deploy_id for d in deployments if not d.is_terminal() and d.state != "live"]
