# Mission 278 - Call Tracer Rewriter (solution)
# An ast.NodeTransformer that instruments functions with call tracing and fixes `== None`.
import ast

TRACE_NAME = "__trace__"


def _docstring_length(body):
    """1 if the first statement is a docstring, else 0."""
    first = body[0] if body else None
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return 1
    return 0


class Instrumenter(ast.NodeTransformer):
    """Insert `__trace__("Qual.name")` at the start of every function body."""

    def __init__(self):
        self.stack = []
        self.rewritten_compares = 0

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()
        return node

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        qualified = ".".join(self.stack)
        self.stack.pop()
        call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id=TRACE_NAME, ctx=ast.Load()),
                args=[ast.Constant(value=qualified)],
                keywords=[],
            )
        )
        node.body.insert(_docstring_length(node.body), call)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Compare(self, node):
        self.generic_visit(node)
        new_ops = []
        for op, right in zip(node.ops, node.comparators):
            is_none = isinstance(right, ast.Constant) and right.value is None
            if is_none and isinstance(op, ast.Eq):
                op = ast.Is()
                self.rewritten_compares += 1
            elif is_none and isinstance(op, ast.NotEq):
                op = ast.IsNot()
                self.rewritten_compares += 1
            new_ops.append(op)
        node.ops = new_ops
        return node


def transform(source, filename="<instrumented>"):
    """Parse, rewrite and compile `source`. Returns (code, transformer)."""
    tree = ast.parse(source, filename)
    transformer = Instrumenter()
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)
    return compile(tree, filename, "exec"), transformer


def run_traced(source, extra=None):
    """Execute instrumented source and return (namespace, list of traced names)."""
    calls = []
    namespace = {TRACE_NAME: calls.append}
    namespace.update(extra or {})
    code, _ = transform(source)
    exec(code, namespace)
    return namespace, calls


if __name__ == "__main__":
    ns, calls = run_traced("def f(x):\n    return x == None\nf(None)\n")
    print(calls)
