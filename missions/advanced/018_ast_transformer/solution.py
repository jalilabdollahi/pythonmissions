# Mission 018 (Advanced) - AST Transformer
# Fixed solution
import ast

class TimingTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        start_stmt = ast.parse("_timing_start = __import__('time').monotonic()").body[0]
        end_stmt = ast.parse("print(f'Elapsed: {__import__('time').monotonic() - _timing_start:.4f}s')").body[0]
        node.body = [start_stmt] + node.body + [end_stmt]
        self.generic_visit(node)
        return node

def instrument_code(source):
    tree = ast.parse(source)
    transformed = TimingTransformer().visit(tree)
    ast.fix_missing_locations(transformed)
    return compile(transformed, "<instrumented>", "exec")
