# Mission 002 - Hostname Mix-Up
# Formats the release-channel message after a rollout.
def deploy_summary(hostname, release, environment):
    env_label = environment.upper()
    return f"{release} deployed to {Hostname} ({env_label})"


def summarize_all(hostnames, release, environment):
    summaries = []
    for host in hostnames:
        summaries.append(deploy_summary(host, release, environment))
    return summaries


if __name__ == "__main__":
    for line in summarize_all(["pay-api-1", "pay-api-2"], "v2.14.0", "prod"):
        print(line)
