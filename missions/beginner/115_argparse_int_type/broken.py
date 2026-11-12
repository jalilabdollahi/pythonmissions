# Mission 115 - Scale Command Parser
# Parses arguments for a command that scales a service in batches.
import argparse
import math


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="scale")
    parser.add_argument("service")
    parser.add_argument("--replicas", default=2)
    parser.add_argument("--batch-size", default=1)
    return parser.parse_args(argv)


def rollout_steps(args):
    return math.ceil(args.replicas / args.batch_size)


def describe(argv):
    args = parse_args(argv)
    steps = rollout_steps(args)
    return f"{args.service}: {args.replicas} replicas in {steps} steps"


if __name__ == "__main__":
    import sys

    print(describe(sys.argv[1:]))
