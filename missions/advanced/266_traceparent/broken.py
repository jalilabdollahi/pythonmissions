# Mission 266 - Traceparent Gatekeeper
# Parse, validate and propagate W3C traceparent headers at an edge proxy.
from collections import namedtuple

HEX = set("0123456789abcdef")

TraceContext = namedtuple("TraceContext", ["version", "trace_id", "span_id", "flags"])


class InvalidTraceparent(ValueError):
    pass


def _is_hex(text, length):
    try:
        int(text, 16)
    except ValueError:
        return False
    return len(text) == length


def parse(header):
    """Parse `version-traceid-spanid-flags`; raise InvalidTraceparent when malformed."""
    if not isinstance(header, str):
        raise InvalidTraceparent("header must be a string")
    parts = header.split("-")
    if len(parts) < 4:
        raise InvalidTraceparent("expected four fields")
    version, trace_id, span_id, flags = parts[:4]
    if not _is_hex(version, 2) or version == "ff":
        raise InvalidTraceparent("bad version")
    if not _is_hex(trace_id, 32):
        raise InvalidTraceparent("bad trace id")
    if not _is_hex(span_id, 16) or span_id == "0" * 16:
        raise InvalidTraceparent("bad parent id")
    if not _is_hex(flags, 2):
        raise InvalidTraceparent("bad flags")
    return TraceContext(version, trace_id, span_id, flags)


def format_header(ctx):
    return f"{ctx.version}-{ctx.trace_id}-{ctx.span_id}-{ctx.flags}"


def is_sampled(ctx):
    return bool(int(ctx.flags, 16) & 1)


def new_span_id(rng):
    """Random non-zero 64-bit id as 16 lowercase hex digits."""
    while True:
        value = rng.getrandbits(64)
        if value != 0:
            return "%x" % value


def child_context(parent, rng):
    """Same trace and sampling decision, fresh span id, always emitted as version 00."""
    return TraceContext("00", parent.trace_id, new_span_id(rng), parent.flags)


def start_trace(rng, sampled=True):
    trace_id = format(rng.getrandbits(128) or 1, "032x")
    return TraceContext("00", trace_id, new_span_id(rng), "01" if sampled else "00")


def continue_or_start(header, rng):
    """Edge behaviour: continue a valid inbound trace, otherwise begin a new one."""
    if header is not None:
        try:
            return child_context(parse(header), rng), True
        except InvalidTraceparent:
            pass
    return start_trace(rng), False


if __name__ == "__main__":
    import random

    ctx, continued = continue_or_start(None, random.Random(1))
    print(format_header(ctx), continued)
