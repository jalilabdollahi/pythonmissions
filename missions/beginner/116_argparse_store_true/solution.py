# Mission 116 - Dry Run Switch (solution)
# Parses the flags of a deploy command, including dry-run and force switches.
import argparse


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="deploytool")
    parser.add_argument("target")
    parser.add_argument("--dry-run", action="store_true", help="preview without changing anything")
    parser.add_argument("--force", action="store_true", help="skip the safety checks")
    return parser.parse_args(argv)


def describe(args):
    if args.dry_run:
        text = f"DRY RUN: would deploy {args.target}"
    else:
        text = f"deploying {args.target}"
    if args.force:
        text += " (forced)"
    return text


def main(argv=None):
    args = parse_args(argv)
    print(describe(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
