# Mission 225 - Swarm Roll Call
# SWIM-style gossip membership table with incarnation numbers and suspicion timeouts.
from collections import namedtuple

Member = namedtuple("Member", ["status", "incarnation", "suspected_at"])

SEVERITY = {"alive": 0, "suspect": 2, "dead": 1}


class Membership:
    def __init__(self, me, clock, suspect_timeout=5.0):
        self.me = me
        self.clock = clock
        self.suspect_timeout = suspect_timeout
        self.members = {me: Member("alive", 0, None)}

    def snapshot(self):
        return {n: (m.status, m.incarnation) for n, m in sorted(self.members.items())}

    def _accepts(self, current, status, incarnation):
        if current is None:
            return True
        if incarnation != current.incarnation:
            return True
        return SEVERITY[status] > SEVERITY[current.status]

    def apply(self, name, status, incarnation):
        current = self.members.get(name)
        if not self._accepts(current, status, incarnation):
            return False
        if name == self.me and status != "alive":
            self.refute(incarnation)
            return True
        suspected_at = self.clock() if status == "suspect" else None
        self.members[name] = Member(status, incarnation, suspected_at)
        return True

    def refute(self, accused_incarnation):
        own = self.members[self.me]
        new_inc = own.incarnation + 1
        self.members[self.me] = Member("alive", new_inc, None)

    def merge(self, remote):
        changed = []
        for name, (status, incarnation) in sorted(remote.items()):
            if self.apply(name, status, incarnation):
                changed.append(name)
        return changed

    def suspect(self, name):
        current = self.members.get(name)
        if current is None or current.status != "alive":
            return False
        return self.apply(name, "suspect", current.incarnation)

    def expire_suspects(self):
        now = self.clock()
        dead = []
        for name, member in sorted(self.members.items()):
            if member.status != "suspect":
                continue
            if now - member.suspected_at > self.suspect_timeout:
                self.members[name] = Member("dead", member.incarnation, None)
                dead.append(name)
        return dead

    def alive_members(self):
        return sorted(n for n, m in self.members.items() if m.status == "alive")

    def summary(self):
        counts = {"alive": 0, "suspect": 0, "dead": 0}
        for member in self.members.values():
            counts[member.status] += 1
        return counts

    def quorum_alive(self):
        return self.summary()["alive"] * 2 > len(self.members)
