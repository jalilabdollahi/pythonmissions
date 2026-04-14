# Mission 023 (Advanced) - Distributed Trace Correlator
# Fix the 2 bugs in this script.

class TraceCorrelator:
    def __init__(self):
        self._spans = {}  # span_id -> span dict

    def add_span(self, span):
        self._spans[span["span_id"]] = span

    def build_tree(self):
        """Build parent-child relationships."""
        roots = []
        children = {}
        for span_id, span in self._spans.items():
            parent_id = span.get("parent_span_id")
            if parent_id is None:
                roots.append(span)
            else:
                children.setdefault(span_id, []).append(span)  # BUG 1: key should be parent_id
        for span in self._spans.values():
            span["children"] = children.get(span["span_id"], [])
        return roots

    def span_duration_ms(self, span_id):
        span = self._spans.get(span_id)
        if not span:
            return None
        return span["start_time"] - span["end_time"]  # BUG 2: should be end - start

    def critical_path(self, root_span_id):
        """Find the longest path through the trace."""
        def dfs(sid):
            span = self._spans.get(sid)
            if not span:
                return 0
            dur = self.span_duration_ms(sid) or 0
            child_max = max((dfs(c["span_id"]) for c in span.get("children", [])), default=0)
            return dur + child_max
        return dfs(root_span_id)
