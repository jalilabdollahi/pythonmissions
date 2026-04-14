# Mission 069 - Classmethod Factory
# Fixed solution

class ServiceConfig:
    def __init__(self, name, host, port, env="prod"):
        self.name = name
        self.host = host
        self.port = port
        self.env = env

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d["name"],
            host=d["host"],
            port=d["port"],
            env=d.get("env", "prod"),
        )

    @classmethod
    def development(cls, name):
        return cls(name=name, host="localhost", port=8080, env="dev")

    def is_prod(self):
        return self.env == "prod"
