# Mission 196 - Edge Cache Console (solution)
# A tiny CDN cache management CLI built from argparse subcommands.
import argparse


def cmd_purge(args):
    return f"purged {len(args.paths)} path(s) in zone {args.zone}"


def cmd_ttl(args):
    minutes = args.seconds // 60
    return f"zone {args.zone} ttl set to {minutes} minute(s)"


def cmd_status(args):
    return f"zone {args.zone} is serving"


def build_parser():
    parser = argparse.ArgumentParser(prog="edgectl", description="Manage CDN cache zones")
    sub = parser.add_subparsers(dest="command", required=True)

    purge = sub.add_parser("purge", help="purge paths from a zone")
    purge.add_argument("zone")
    purge.add_argument("paths", nargs="+")
    purge.set_defaults(func=cmd_purge)

    ttl = sub.add_parser("ttl", help="change the default TTL of a zone")
    ttl.add_argument("zone")
    ttl.add_argument("seconds", type=int)

    ttl.set_defaults(func=cmd_ttl)

    status = sub.add_parser("status", help="show zone status")
    status.add_argument("zone")
    status.set_defaults(func=cmd_status)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    print(main())
