# Mission 081 - Dockerfile Linter
# Fixed solution

def lint_dockerfile(content):
    lines = [l.strip() for l in content.strip().splitlines()]
    issues = []

    for i, line in enumerate(lines, 1):
        if line.startswith("FROM") and ":latest" in line:
            issues.append(f"Line {i}: avoid using :latest tag")

    run_streak = 0
    for i, line in enumerate(lines, 1):
        if line.startswith("RUN"):
            run_streak += 1
            if run_streak > 1:
                issues.append(f"Line {i}: combine RUN instructions with &&")
        else:
            run_streak = 0

    return issues
