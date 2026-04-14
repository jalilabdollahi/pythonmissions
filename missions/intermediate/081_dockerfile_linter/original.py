# Mission 081 - Dockerfile Linter
# Fix the 2 bugs in this script.

def lint_dockerfile(content):
    lines = [l.strip() for l in content.strip().splitlines()]
    issues = []

    # Check for latest tag usage
    for i, line in enumerate(lines, 1):
        if line.startswith("FROM") and ":latest" not in line:  # BUG 1: logic inverted
            issues.append(f"Line {i}: avoid using :latest tag")

    # Check for multiple consecutive RUN statements
    prev_was_run = False
    run_streak = 0
    for i, line in enumerate(lines, 1):
        if line.startswith("RUN"):
            run_streak += 1
            if run_streak > 1:
                issues.append(f"Line {i}: combine RUN instructions with &&")
        else:
            run_streak = 0

    return issues
