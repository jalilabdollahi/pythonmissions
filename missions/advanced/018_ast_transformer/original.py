# Mission 018 (Advanced) - AST Transformer
# Fix the 2 bugs in this script.
import ast

class TimingTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Prepend timing_start = time.monotonic() to function body
        start_stmt = ast.parse("_timing_start = __import__('time').monotonic()").body[0]
        end_stmt = ast.parse("print(f'Elapsed: {__import__('time').monotonic() - _timing_start:.4f}s')").body[0]
        node.body = [start_stmt] + node.body + [end_stmt]
        return node  # BUG 1: must call self.generic_visit(node) to recurse into nested functions

def instrument_code(source):
    tree = ast.parse(source)
    transformed = TimingTransformer().visit(tree)
    # BUG 2: must call ast.fix_missing_locations(transformed) before compile
    return compile(transformed, "<instrumented>", "exec")
