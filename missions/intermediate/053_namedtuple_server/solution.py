# Mission 053 - Named Tuple Server Record
# Fixed solution
from collections import namedtuple

Server = namedtuple("Server", ["hostname", "ip", "port", "env"])

def make_server(hostname, ip, port, env="prod"):
    return Server(hostname, ip, port, env)

def server_url(server):
    return f"http://{server.hostname}:{server.port}"

def is_production(server):
    return server.env == "prod"
