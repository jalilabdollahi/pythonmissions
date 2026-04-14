# Mission 053 - Named Tuple Server Record
# Fix the 2 bugs in this script.
from collections import namedtuple

Server = namedtuple("Server", ["hostname", "ip", "port", "env"])

def make_server(hostname, ip, port, env="prod"):
    return Server(hostname, ip, port, env)

def server_url(server):
    return f"http://{server.host}:{server.port}"  # BUG 1: field is "hostname" not "host"

def is_production(server):
    return server.environment == "prod"  # BUG 2: field is "env" not "environment"
