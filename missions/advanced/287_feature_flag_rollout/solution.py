# Mission 287 - Gradual Rollout Gate (solution)
# Percentage feature-flag rollout with stable per-user bucketing, allow/deny lists and a kill switch.
import hashlib

BUCKETS = 10000


def _hash(text):
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def bucket(flag_name, user_id):
    """Map a user to one of 10,000 buckets, independently for every flag."""
    return _hash(f"{flag_name}:{user_id}") % BUCKETS


class Flag:
    def __init__(self, name, percent=0.0, enabled=True, allow=(), deny=()):
        self.name = name
        self.percent = percent
        self.enabled = enabled
        self.allow = set(allow)
        self.deny = set(deny)


def is_enabled(flag, user_id):
    """Decide whether this user sees the feature.

    Order of precedence: kill switch, deny list, allow list, percentage.
    """
    if not flag.enabled:
        return False
    if user_id in flag.deny:
        return False
    if user_id in flag.allow:
        return True
    threshold = round(flag.percent * 100)
    return bucket(flag.name, user_id) < threshold


def cohort(flag, user_ids):
    return {u for u in user_ids if is_enabled(flag, u)}


def ramp_is_safe(flag, user_ids, new_percent):
    """True when raising the rollout keeps every user who already had the feature."""
    before = cohort(flag, user_ids)
    raised = Flag(flag.name, new_percent, flag.enabled, flag.allow, flag.deny)
    return new_percent >= flag.percent and before <= cohort(raised, user_ids)


def exposure(flag, user_ids):
    users = list(user_ids)
    if not users:
        return 0.0
    return len(cohort(flag, users)) / len(users)


def next_step(current, schedule):
    """The next rollout percentage on the ramp schedule, or None when fully rolled out."""
    for step in sorted(schedule):
        if step > current:
            return step
    return None


class FlagStore:
    def __init__(self, flags=()):
        self._flags = {f.name: f for f in flags}

    def check(self, name, user_id):
        """Unknown flags are off: a typo must never ship a feature to everyone."""
        flag = self._flags.get(name)
        return flag is not None and is_enabled(flag, user_id)

    def advance(self, name, schedule):
        flag = self._flags[name]
        step = next_step(flag.percent, schedule)
        if step is not None:
            flag.percent = step
        return flag.percent


if __name__ == "__main__":
    demo = Flag("checkout-v2", percent=25)
    print(exposure(demo, [f"user-{i}" for i in range(1000)]))
