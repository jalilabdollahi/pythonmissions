# Mission 023 - Custom Exception Hierarchy
# Fix the 2 bugs in this script.

class DeploymentError(object):  # BUG 1: should inherit from Exception
    pass

class NetworkError(DeploymentError):
    pass

class TimeoutError(NetworkError):
    pass

def deploy(service, timeout=30):
    if not service:
        raise DeploymentError("Service name is required")
    if timeout < 0:
        raise TimeoutError("Timeout must be positive")
    return f"Deployed {service}"

def safe_deploy(service, timeout=30):
    try:
        return deploy(service, timeout)
    except DeploymentError:  # BUG 2: broader exception before specific one (TimeoutError)
        return "deployment failed"
    except TimeoutError:
        return "timed out"
