# Mission 054 - Functools Partial
# Fix the 2 bugs in this script.
import functools

def deploy(service, env, replicas=1, dry_run=False):
    return {"service": service, "env": env, "replicas": replicas, "dry_run": dry_run}

def make_deployer(env):
    # Create a deployer pre-configured for the given environment
    return functools.partial(deploy, env)  # BUG 1: binds env as first arg (service), should use keyword

def dry_deploy(service, env):
    # Deploy with dry_run=True
    return deploy(service, env, dry_run="false")  # BUG 2: should be False (bool not string)
