# Mission 259 - Rolling Update Planner (solution)
# Plans the pod-by-pod steps of a rolling update from maxSurge / maxUnavailable settings.
from collections import namedtuple

Step = namedtuple("Step", ["old", "new", "ready"])


def resolve(value, replicas, round_up):
    """Turn an int or a 'NN%' string into a pod count."""
    if isinstance(value, bool):
        raise ValueError("limits must be an int or a percentage string")
    if isinstance(value, int):
        if value < 0:
            raise ValueError("limits cannot be negative")
        return value
    if isinstance(value, str) and value.endswith("%") and value[:-1].isdigit():
        percent = int(value[:-1])
        scaled = percent * replicas
        return -(-scaled // 100) if round_up else scaled // 100
    raise ValueError(f"cannot interpret limit {value!r}")


def resolve_limits(replicas, max_surge, max_unavailable):
    if replicas < 1:
        raise ValueError("replicas must be at least 1")
    surge = resolve(max_surge, replicas, round_up=True)
    unavailable = resolve(max_unavailable, replicas, round_up=False)
    if surge == 0 and unavailable == 0:
        unavailable = 1
    return surge, min(unavailable, replicas)


def plan_rollout(replicas, max_surge="25%", max_unavailable="25%"):
    """Return the list of Steps. New pods only count as ready from the following step."""
    surge, unavailable = resolve_limits(replicas, max_surge, max_unavailable)
    min_ready = replicas - unavailable
    old, new, ready_new = replicas, 0, 0
    steps = []
    while old > 0 or new < replicas:
        room = replicas + surge - (old + new)
        created = max(0, min(replicas - new, room))
        removable = max(0, min(old, old + ready_new - min_ready))
        old -= removable
        steps.append(Step(old, new + created, old + ready_new))
        newly_ready = new + created != ready_new
        new += created
        ready_new = new
        if created == 0 and removable == 0 and not newly_ready:
            raise RuntimeError("rollout cannot make progress with these limits")
    return steps


def check_plan(replicas, steps, max_surge, max_unavailable):
    """Return a list of human readable violations (empty means the plan is safe)."""
    surge, unavailable = resolve_limits(replicas, max_surge, max_unavailable)
    problems = []
    for index, step in enumerate(steps, start=1):
        if step.old + step.new > replicas + surge:
            problems.append(f"step {index}: {step.old + step.new} pods exceeds surge limit")
        if step.ready < replicas - unavailable:
            problems.append(f"step {index}: only {step.ready} ready pods")
    if not steps or (steps[-1].old, steps[-1].new) != (0, replicas):
        problems.append("rollout does not finish on the new version")
    return problems


def peak_pods(steps, replicas):
    """Most pods that exist at the end of any rollout round."""
    return max([replicas] + [step.old + step.new for step in steps])


def describe(replicas, max_surge, max_unavailable):
    steps = plan_rollout(replicas, max_surge, max_unavailable)
    return f"{replicas} replicas -> {len(steps)} steps, final {steps[-1].new} new"
