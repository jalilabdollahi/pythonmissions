# Mission 013 - Identity Crisis In Prod (solution)
# Decides whether a deployment target needs manual approval.
PROTECTED = "prod"


def needs_approval(environment):
    normalized = environment.strip().lower()
    return normalized == PROTECTED


def deploy_gate(environment):
    if needs_approval(environment):
        return "manual approval required"
    return "auto deploy"


if __name__ == "__main__":
    import sys

    print(deploy_gate(sys.argv[1] if len(sys.argv) > 1 else "staging"))
