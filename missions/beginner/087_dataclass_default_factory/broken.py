# Mission 087 - Release Manifest Dataclass
# Models a deployment release with its services and notes.
from dataclasses import dataclass, field


@dataclass
class Release:
    version: str
    services: list = []
    notes: list = []

    def add_service(self, name):
        self.services.append(name)
        return self

    def add_note(self, text):
        self.notes.append(text)
        return self

    def summary(self):
        names = ", ".join(self.services) or "none"
        return f"{self.version}: {names} ({len(self.notes)} notes)"


def release_train(versions):
    return [Release(v) for v in versions]


if __name__ == "__main__":
    r = Release("1.2.0").add_service("api").add_service("web").add_note("hotfix")
    print(r.summary())
