# Mission 091 - OpenTelemetry Span
# Fixed solution
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    provider = TracerProvider()
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
except ImportError:
    class _Span:
        def __init__(self): self.attrs = {}; self.ended = False
        def set_attribute(self, k, v): self.attrs[k] = v
        def end(self): self.ended = True
        def __enter__(self): return self
        def __exit__(self, *a): self.end()
    class _Tracer:
        def start_span(self, name): return _Span()
        def start_as_current_span(self, name):
            import contextlib
            @contextlib.contextmanager
            def ctx():
                s = _Span()
                yield s
                s.end()
            return ctx()
    tracer = _Tracer()

def trace_request(method, path, status_code):
    span = tracer.start_span("http.request")
    span.set_attribute("http.method", method)
    span.set_attribute("http.path", path)
    span.set_attribute("http.status_code", status_code)
    span.end()
    return span
