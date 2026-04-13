# Mission 04 - Parse Args
# Fix the 2 bugs in this script.

import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Deploy a service to an environment.")
    parser.add_argument("--env", required=True, help="Target environment (staging/production)")
    parser.add_argument("--version", default="latest", help="Version to deploy")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deployment only")
    return parser


def run_deploy(args):
    environment = args.environment
    version = args.version
    dry_run = args.dry-run

    if dry_run:
        return f"[DRY RUN] Would deploy {version} to {environment}"
    return f"Deploying {version} to {environment}"


def main():
    parser = create_parser()
    args = parser.parse_args()
    print(run_deploy(args))


if __name__ == "__main__":
    main()
