# Mission 05 - Format Output
# Fix the 2 bugs in this script.

from datetime import datetime


def format_deploy_message(service, version, environment, deployer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = "[DEPLOY] %s v%s -> %s" % (service, version)

    body = "Deployed by: {}".format()

    return {
        "subject": subject,
        "body": body,
        "timestamp": timestamp,
        "full": f"{subject}\n{body}\nTime: {timestamp}",
    }


if __name__ == "__main__":
    msg = format_deploy_message(
        service="api-gateway",
        version="3.1.4",
        environment="production",
        deployer="jalil",
    )
    print(msg["full"])
