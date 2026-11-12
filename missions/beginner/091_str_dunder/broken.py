# Mission 091 - Printable Deployment Records
# Deployment objects that read well in chat and logs.


class Deployment:
    def __init__(self, service, version, env, ok=True):
        self.service = service
        self.version = version
        self.env = env
        self.ok = ok

    def __str__(self):
        state = "OK" if self.ok else "FAILED"
        return (self.service, self.version, self.env, state)

    def __repr__(self):
        return f"Deployment({self.service!r}, {self.version!r}, {self.env!r})"


def changelog(deployments):
    return "\n".join(str(d) for d in deployments)


def failures(deployments):
    return [d for d in deployments if not d.ok]


if __name__ == "__main__":
    log = [Deployment("api", "2.3.1", "prod"), Deployment("web", "9.0.0", "stage", ok=False)]
    print(changelog(log))
