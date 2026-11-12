# Mission 028 - Frozen Launch Flags
# Build variants of the immutable worker launch flags.

BASE_ARGS = ("--workers", "4", "--log-level", "info", "--no-color")


def with_extra_args(base, extra):
    merged = base
    merged.extend(extra)
    return tuple(merged)


def quiet_variant(base):
    args = base
    level_pos = args.index("--log-level") + 1
    args[level_pos] = "error"
    return tuple(args)


def launch_command(binary, args):
    return " ".join((binary,) + tuple(args))
