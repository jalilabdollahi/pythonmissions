# Mission 300 - Release Train Conductor (solution)
# Capstone: a CD orchestrator with dependency ordering, a deployment state machine,
# approval gates and automatic rollback.

TRANSITIONS = {
    "pending": {"deploying"},
    "deploying": {"verifying", "failed"},
    "verifying": {"live", "failed"},
    "live": {"rolling_back"},
    "failed": {"rolling_back"},
    "rolling_back": {"rolled_back", "rollback_failed"},
    "rolled_back": set(),
    "rollback_failed": set(),
}


class CycleError(Exception):
    pass


class IllegalTransition(Exception):
    pass


class DeployError(Exception):
    pass


class ServiceRun:
    """One service's progress through a stage, guarded by the transition table."""

    def __init__(self, name):
        self.name = name
        self.state = "pending"
        self.history = ["pending"]

    def move(self, new_state):
        if new_state not in TRANSITIONS[self.state]:
            raise IllegalTransition(f"{self.name}: {self.state} -> {new_state}")
        self.state = new_state
        self.history.append(new_state)


def plan_order(versions, depends_on):
    """Deployment order for the services in a release: dependencies first, ties alphabetical.

    Dependencies that are not part of this release are assumed to be deployed already.
    """
    wanted = set(versions)
    indegree = {
        svc: len([d for d in depends_on.get(svc, ()) if d in wanted]) for svc in sorted(wanted)
    }
    dependents = {svc: [] for svc in wanted}
    for svc in wanted:
        for dep in depends_on.get(svc, ()):
            if dep in wanted:
                dependents[dep].append(svc)
    ready = sorted(svc for svc, count in indegree.items() if count == 0)
    order = []
    while ready:
        svc = ready.pop(0)
        order.append(svc)
        for child in dependents[svc]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort()
    if len(order) != len(wanted):
        stuck = sorted(wanted - set(order))
        raise CycleError(f"dependency cycle among {stuck}")
    return order


class ApprovalBook:
    """Collects approvals; a release needs `required` DISTINCT, recent reviewers other than its author."""

    def __init__(self, clock, required=2, ttl=3600):
        self.clock = clock
        self.required = required
        self.ttl = ttl
        self._votes = {}

    def approve(self, release_id, user):
        self._votes.setdefault(release_id, []).append((user, self.clock()))

    def valid_approvers(self, release_id, author):
        now = self.clock()
        return {
            user
            for user, stamp in self._votes.get(release_id, [])
            if user != author and now - stamp <= self.ttl
        }

    def is_approved(self, release_id, author):
        return len(self.valid_approvers(release_id, author)) >= self.required


class FakeDeployer:
    """In-memory deploy target. Failures are keyed by (env, service, version)."""

    def __init__(self, fail_deploy=(), unhealthy=()):
        self.fail_deploy = set(fail_deploy)
        self.unhealthy = set(unhealthy)
        self.live = {}
        self.calls = []

    def deploy(self, env, service, version):
        self.calls.append(("deploy", env, service, version))
        if (env, service, version) in self.fail_deploy:
            raise DeployError(f"{service} {version} failed to start in {env}")
        self.live[(env, service)] = version

    def healthy(self, env, service, version):
        return (env, service, version) not in self.unhealthy

    def remove(self, env, service):
        self.calls.append(("remove", env, service))
        self.live.pop((env, service), None)


class Orchestrator:
    def __init__(self, deployer, depends_on, current, approvals,
                 stages=("staging", "prod"), gated=("prod",)):
        self.deployer = deployer
        self.depends_on = depends_on
        self.current = {env: dict(versions) for env, versions in current.items()}
        self.approvals = approvals
        self.stages = stages
        self.gated = gated
        self.runs = {}

    def release(self, release_id, author, versions):
        order = plan_order(versions, self.depends_on)
        report = {"release": release_id, "status": "succeeded", "stages": {}, "blocked_at": None}
        for env in self.stages:
            if env in self.gated and not self.approvals.is_approved(release_id, author):
                report["status"] = "awaiting_approval"
                report["blocked_at"] = env
                return report
            outcome = self._deploy_stage(env, order, versions)
            report["stages"][env] = outcome
            if outcome != "live":
                report["status"] = outcome
                return report
            self.current[env].update(versions)
        return report

    def _deploy_stage(self, env, order, versions):
        previous = dict(self.current[env])
        runs = []
        failed = False
        for service in order:
            run = ServiceRun(service)
            runs.append(run)
            run.move("deploying")
            try:
                self.deployer.deploy(env, service, versions[service])
                run.move("verifying")
                if not self.deployer.healthy(env, service, versions[service]):
                    raise DeployError(f"{service} failed its health check")
            except DeployError:
                run.move("failed")
                failed = True
                break
            run.move("live")
        self.runs[env] = runs
        if not failed:
            return "live"
        return self._roll_back(env, runs, previous)

    def _roll_back(self, env, runs, previous):
        incomplete = False
        for run in reversed(runs):
            run.move("rolling_back")
            try:
                if run.name in previous:
                    self.deployer.deploy(env, run.name, previous[run.name])
                else:
                    self.deployer.remove(env, run.name)
                run.move("rolled_back")
            except DeployError:
                run.move("rollback_failed")
                incomplete = True
        return "rollback_incomplete" if incomplete else "rolled_back"

    def states(self, env):
        return {run.name: run.state for run in self.runs.get(env, [])}
