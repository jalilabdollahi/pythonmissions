# Mission 023 - Custom Exception Hierarchy
# Fixed solution

class DeploymentError(Exception):
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
    except TimeoutError:
        return "timed out"
    except DeploymentError:
        return "deployment failed"
