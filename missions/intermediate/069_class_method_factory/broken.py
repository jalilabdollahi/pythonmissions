# Mission 069 - Classmethod Factory
# Fix the 2 bugs in this script.

class ServiceConfig:
    def __init__(self, name, host, port, env="prod"):
        self.name = name
        self.host = host
        self.port = port
        self.env = env

    @classmethod
    def from_dict(cls, d):
        return ServiceConfig(  # BUG 1: should use cls() not ServiceConfig()
            name=d["name"],
            host=d["host"],
            port=d["port"],
            env=d.get("env", "prod"),
        )

    @classmethod
    def development(cls, name):
        return cls(name=name, host="localhost", port=8080)  # BUG 2: missing env="dev"

    def is_prod(self):
        return self.env == "prod"
