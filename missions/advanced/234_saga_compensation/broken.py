# Mission 234 - Environment Spin-Up Undo
# Saga orchestrator that provisions a preview environment and undoes it on failure.
from collections import namedtuple

Step = namedtuple("Step", ["name", "action", "compensate"])


def run_saga(steps, context):
    completed = []
    failure = None
    for step in steps:
        try:
            result = step.action(context)
        except Exception as exc:
            failure = (step.name, str(exc))
            completed.append((step, None))
            break
        completed.append((step, result))
    if failure is None:
        return {
            "status": "completed",
            "completed": [s.name for s, _ in completed],
            "compensated": [],
            "compensation_errors": [],
            "failure": None,
        }
    compensated = []
    errors = []
    for step, result in completed:
        try:
            step.compensate(completed[-1][1])
            compensated.append(step.name)
        except Exception as exc:
            errors.append((step.name, str(exc)))
            break
    return {
        "status": "rolled_back" if not errors else "rollback_incomplete",
        "completed": [s.name for s, _ in completed],
        "compensated": compensated,
        "compensation_errors": errors,
        "failure": failure,
    }


class FakeCloud:
    def __init__(self, fail_on=None, fail_delete=()):
        self.resources = {}
        self.fail_on = fail_on
        self.fail_delete = set(fail_delete)
        self.calls = []
        self._ids = 0

    def create(self, kind):
        self.calls.append(("create", kind))
        if kind == self.fail_on:
            raise RuntimeError(f"quota exceeded creating {kind}")
        self._ids += 1
        handle = f"{kind}-{self._ids}"
        self.resources[handle] = kind
        return handle

    def delete(self, handle):
        self.calls.append(("delete", handle))
        kind = self.resources.get(handle)
        if kind is None:
            raise KeyError(f"{handle} does not exist")
        if kind in self.fail_delete:
            raise RuntimeError(f"cannot delete {kind} right now")
        del self.resources[handle]


def preview_environment(cloud):
    def step(kind):
        return Step(kind, lambda ctx: cloud.create(kind), cloud.delete)

    return [step("network"), step("database"), step("dns"), step("deploy")]
