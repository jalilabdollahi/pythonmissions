# Mission 294 - Hedged Requests
# Simulate hedged (backup) requests on a fake timeline: the first SUCCESS wins.


class AllAttemptsFailed(Exception):
    pass


class Replica:
    def __init__(self, name, latency, fail=False):
        self.name = name
        self.latency = latency
        self.fail = fail


class Attempt:
    def __init__(self, replica, start):
        self.name = replica.name
        self.start = start
        self.finish = replica.latency
        self.fail = replica.fail


class HedgeResult:
    def __init__(self, winner, finished_at, launched, cancelled):
        self.winner = winner
        self.finished_at = finished_at
        self.launched = launched
        self.cancelled = cancelled

    def __repr__(self):
        return f"HedgeResult({self.winner} at {self.finished_at}, launched={self.launched})"


def hedged_call(replicas, hedge_delay):
    """Send the request to replica 0 at t=0, then to the next replica every `hedge_delay`.

    A hedge is only sent if no success has finished by its launch time. The winner is the
    successful attempt that FINISHES first. Attempts still running at that moment are cancelled.
    """
    attempts = []
    best = None
    for index, replica in enumerate(replicas):
        start = index * hedge_delay
        if best is not None and best.finish < start:
            break
        attempt = Attempt(replica, start)
        attempts.append(attempt)
        if best is None or attempt.finish < best.finish:
            best = attempt
    if best is None:
        raise AllAttemptsFailed([a.name for a in attempts])
    cancelled = [a.name for a in attempts if a is not best]
    return HedgeResult(best.name, best.finish, len(attempts), cancelled)


def latency_saved(replicas, hedge_delay):
    """How much sooner the hedged call finishes than waiting for replica 0 alone."""
    result = hedged_call(replicas, hedge_delay)
    return replicas[0].latency - result.finished_at


def extra_load(replicas, hedge_delay):
    """Number of duplicate requests the hedging policy sent."""
    return hedged_call(replicas, hedge_delay).launched - 1


if __name__ == "__main__":
    fleet = [Replica("us-east", 4.0), Replica("us-west", 0.8), Replica("eu", 1.2)]
    print(hedged_call(fleet, 1.0))
