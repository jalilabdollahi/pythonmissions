# Mission 270 - Stackweaver Apply Order
# Turn a resource dependency graph into parallel apply batches, and tear it down in reverse.


class CycleError(Exception):
    def __init__(self, path):
        super().__init__("dependency cycle: " + " -> ".join(path))
        self.path = path


class MissingDependency(Exception):
    pass


def validate(graph):
    for name in sorted(graph):
        for dep in graph[name]:
            if dep not in graph:
                raise MissingDependency(f"{name} depends on unknown resource {dep}")


def levels(graph):
    """graph: name -> list of dependencies. Returns batches that may run in parallel.

    A resource sits one level above its deepest dependency.
    """
    depth = {}
    visiting = []

    def visit(name):
        if name in depth:
            return depth[name]
        if name in visiting:
            raise CycleError(visiting[visiting.index(name):] + [name])
        visiting.append(name)
        depth[name] = 1 + min((visit(dep) for dep in graph[name]), default=-1)
        visiting.pop()
        return depth[name]

    for name in sorted(graph):
        visit(name)
    batches = [[] for _ in range(max(depth.values(), default=-1) + 1)]
    for name in sorted(depth):
        batches[depth[name]].append(name)
    return batches


def apply_all(graph, action):
    """Create resources dependency-first. Failed resources block everything downstream.

    Returns {name: "ok" | "failed" | "skipped"} and the batches that were attempted.
    """
    status = {}
    attempted = []
    for batch in levels(graph):
        run = []
        for name in batch:
            if any(status[dep] == "failed" for dep in graph[name]):
                status[name] = "skipped"
                continue
            run.append(name)
            try:
                action(name)
                status[name] = "ok"
            except Exception:
                status[name] = "failed"
        attempted.append(run)
    return status, attempted


def destroy_all(graph, action):
    """Delete dependents before the things they depend on."""
    dependents = {name: [] for name in graph}
    for name, deps in graph.items():
        for dep in deps:
            dependents[dep].append(name)
    status = {}
    attempted = []
    for batch in levels(graph):
        run = []
        for name in batch:
            if any(status[d] != "ok" for d in dependents[name]):
                status[name] = "skipped"
                continue
            run.append(name)
            try:
                action(name)
                status[name] = "ok"
            except Exception:
                status[name] = "failed"
        attempted.append(run)
    return status, attempted


def describe(graph):
    return [f"level {i}: {', '.join(batch)}" for i, batch in enumerate(levels(graph))]


if __name__ == "__main__":
    stack = {"vpc": [], "subnet": ["vpc"], "db": ["subnet"], "app": ["db", "subnet"]}
    print(describe(stack))
