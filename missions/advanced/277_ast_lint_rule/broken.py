# Mission 277 - Event Loop Blocker Lint
# A lint rule that finds blocking calls inside `async def` bodies using ast.NodeVisitor.
import ast
from collections import namedtuple

Finding = namedtuple("Finding", ["line", "col", "code", "message"])

BLOCKING = {
    "time.sleep": "use asyncio.sleep",
    "subprocess.run": "use asyncio.create_subprocess_exec",
    "requests.get": "use an async HTTP client",
    "requests.post": "use an async HTTP client",
}


class BlockingCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.aliases = {}  # local name -> dotted target
        self.async_depth = []  # stack of booleans: is the innermost function async?
        self.findings = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname:
                self.aliases[alias.asname] = alias.name
            else:
                top = alias.name.split(".")[0]
                self.aliases[top] = top

    def visit_ImportFrom(self, node):
        if node.level or not node.module:
            return
        for alias in node.names:
            self.aliases[alias.name] = f"{node.module}.{alias.name}"

    def visit_AsyncFunctionDef(self, node):
        self.async_depth.append(True)
        self.generic_visit(node)
        self.async_depth.pop()

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

    def visit_Lambda(self, node):
        self.async_depth.append(False)
        self.generic_visit(node)
        self.async_depth.pop()

    def dotted_name(self, func):
        parts = []
        while isinstance(func, ast.Attribute):
            parts.append(func.attr)
            func = func.value
        if not isinstance(func, ast.Name):
            return None
        base = self.aliases.get(func.id, func.id)
        return ".".join([base] + list(reversed(parts)))

    def visit_Call(self, node):
        if self.async_depth and self.async_depth[-1]:
            name = self.dotted_name(node.func)
            if name in BLOCKING:
                self.findings.append(
                    Finding(node.end_lineno, node.col_offset + 1, "ASYNC100", f"{name}() blocks the event loop; {BLOCKING[name]}")
                )


def lint_source(source):
    """Return findings sorted by position; a syntax error becomes a single E999 finding."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [Finding(exc.lineno or 1, (exc.offset or 0), "E999", f"syntax error: {exc.msg}")]
    visitor = BlockingCallVisitor()
    visitor.visit(tree)
    return sorted(visitor.findings, key=lambda f: (f.line, f.col))


def format_findings(findings, filename="<string>"):
    return [f"{filename}:{f.line}:{f.col}: {f.code} {f.message}" for f in findings]


if __name__ == "__main__":
    demo = "import time\nasync def f():\n    time.sleep(1)\n"
    print("\n".join(format_findings(lint_source(demo), "demo.py")))
