# Mission 054 - Functools Partial
# Fixed solution
import functools

def deploy(service, env, replicas=1, dry_run=False):
    return {"service": service, "env": env, "replicas": replicas, "dry_run": dry_run}

def make_deployer(env):
    return functools.partial(deploy, env=env)

def dry_deploy(service, env):
    return deploy(service, env, dry_run=True)
