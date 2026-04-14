# Mission 020 - CLI Argument Parser
# Fix the 2 bugs in this script.
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="Deploy a service")
    parser.add_argument("env", help="Target environment (dev/staging/prod)")
    parser.add_argument("-port", type=str, default=8080,  # BUG 1: should be --port and type=int
                        help="Port to deploy on")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    return parser

def parse_deploy_args(args=None):
    parser = build_parser()
    return parser.parse_args(args)
