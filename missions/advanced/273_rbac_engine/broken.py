# Mission 273 - Cormorant Access Judge
# Role-based access control with glob patterns, role inheritance and explicit deny.
import re


def glob_to_regex(pattern):
    """`*` matches any run of characters; everything else is literal."""
    escaped = pattern.replace("*", ".*")
    return re.compile(escaped)


def matches(pattern, value):
    return glob_to_regex(pattern).match(value) is not None


class Statement:
    def __init__(self, sid, effect, actions, resources):
        if effect not in ("allow", "deny"):
            raise ValueError(f"unknown effect {effect!r}")
        self.sid = sid
        self.effect = effect
        self.actions = list(actions)
        self.resources = list(resources)

    def applies(self, action, resource):
        return any(matches(a, action) for a in self.actions) and any(
            matches(r, resource) for r in self.resources
        )


class Policy:
    def __init__(self):
        self.roles = {}  # role -> {"inherits": [...], "statements": [Statement]}
        self.users = {}  # user -> [roles]

    def add_role(self, name, statements=(), inherits=()):
        self.roles[name] = {"inherits": list(inherits), "statements": list(statements)}

    def assign(self, user, *roles):
        self.users.setdefault(user, []).extend(roles)

    def effective_roles(self, user):
        seen = set()
        stack = list(self.users.get(user, []))
        while stack:
            role = stack.pop()
            if role in seen or role not in self.roles:
                continue
            seen.add(role)
        return seen

    def explain(self, user, action, resource):
        """Return (decision, sid). Deny beats allow; no match means implicit deny."""
        allowed_by = None
        for role in sorted(self.effective_roles(user)):
            for stmt in self.roles[role]["statements"]:
                if not stmt.applies(action, resource):
                    continue
                if stmt.effect == "deny":
                    if allowed_by is None:
                        return "deny", stmt.sid
                elif allowed_by is None:
                    allowed_by = stmt.sid
        if allowed_by is not None:
            return "allow", allowed_by
        return "deny", None

    def can(self, user, action, resource):
        return self.explain(user, action, resource)[0] == "allow"


def allowed_actions(policy, user, candidates, resource):
    return [a for a in candidates if policy.can(user, a, resource)]


if __name__ == "__main__":
    p = Policy()
    p.add_role("reader", [Statement("r1", "allow", ["s3:Get*"], ["arn:logs/*"])])
    p.assign("kim", "reader")
    print(p.explain("kim", "s3:GetObject", "arn:logs/app.log"))
