# Mission 030 (Advanced) - Continuous Deployment Engine
# Fix the 2 bugs in this script.

class CDEngine:
    ENVIRONMENTS = ["dev", "staging", "prod"]

    def __init__(self):
        self._deployments = {}  # env -> {version, status}
        self._gates = {}        # (from_env, to_env) -> [check_fns]
        self._rollback_history = {}

    def add_gate(self, from_env, to_env, check_fn):
        key = (from_env, to_env)
        self._gates.setdefault(key, []).append(check_fn)

    def deploy(self, version, env):
        self._deployments[env] = {"version": version, "status": "deployed"}

    def can_promote(self, from_env, to_env):
        """Returns True if all gate checks pass."""
        gates = self._gates.get((from_env, to_env), [])
        deployment = self._deployments.get(from_env)
        if not deployment:
            return False
        return any(check(deployment) for check in gates)  # BUG 1: should be all(), not any()

    def promote(self, from_env, to_env):
        if not self.can_promote(from_env, to_env):
            raise RuntimeError(f"Gate check failed: {from_env} -> {to_env}")
        version = self._deployments[from_env]["version"]
        self.deploy(version, to_env)
        return version

    def auto_rollback(self, env, health_check_fn):
        """Roll back if health check passes."""  # docstring is wrong
        deployment = self._deployments.get(env)
        if not deployment:
            return False
        if health_check_fn(deployment):  # BUG 2: should rollback when check FAILS (not passes)
            prev = self._rollback_history.get(env)
            if prev:
                self.deploy(prev["version"], env)
                return True
        return False
