# Mission 030 (Advanced) - Continuous Deployment Engine
# Fixed solution

class CDEngine:
    ENVIRONMENTS = ["dev", "staging", "prod"]

    def __init__(self):
        self._deployments = {}
        self._gates = {}
        self._rollback_history = {}

    def add_gate(self, from_env, to_env, check_fn):
        key = (from_env, to_env)
        self._gates.setdefault(key, []).append(check_fn)

    def deploy(self, version, env):
        if env in self._deployments:
            self._rollback_history[env] = self._deployments[env]
        self._deployments[env] = {"version": version, "status": "deployed"}

    def can_promote(self, from_env, to_env):
        gates = self._gates.get((from_env, to_env), [])
        deployment = self._deployments.get(from_env)
        if not deployment:
            return False
        return all(check(deployment) for check in gates)

    def promote(self, from_env, to_env):
        if not self.can_promote(from_env, to_env):
            raise RuntimeError(f"Gate check failed: {from_env} -> {to_env}")
        version = self._deployments[from_env]["version"]
        self.deploy(version, to_env)
        return version

    def auto_rollback(self, env, health_check_fn):
        """Roll back if health check fails."""
        deployment = self._deployments.get(env)
        if not deployment:
            return False
        if not health_check_fn(deployment):
            prev = self._rollback_history.get(env)
            if prev:
                self._deployments[env] = prev
                return True
        return False
