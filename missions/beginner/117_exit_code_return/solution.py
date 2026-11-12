# Mission 117 - Preflight Exit Status (solution)
# Runs resource checks and reports the result through the process exit code.
import argparse

DISK_LIMIT = 90
MEMORY_LIMIT = 85


def evaluate(disk_used, memory_used):
    return [
        ("disk", disk_used, disk_used < DISK_LIMIT),
        ("memory", memory_used, memory_used < MEMORY_LIMIT),
    ]


def build_parser():
    parser = argparse.ArgumentParser(prog="preflight")
    parser.add_argument("--disk", type=int, required=True)
    parser.add_argument("--memory", type=int, required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    failed = 0
    for name, used, ok in evaluate(args.disk, args.memory):
        label = "PASS" if ok else "FAIL"
        print(f"{label} {name} {used}%")
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
