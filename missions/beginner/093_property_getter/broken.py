# Mission 093 - Uptime Is Not a Method
# Router model with computed, read-only uptime values.


class Router:
    def __init__(self, name, boot_time, now):
        self.name = name
        self.boot_time = boot_time
        self.now = now

    @property
    def uptime_seconds(self):
        return self.now - self.boot_time

    def uptime_hours(self):
        return self.uptime_seconds / 3600

    def is_fresh(self):
        return self.uptime_hours < 1


def status_line(router):
    return f"{router.name} up {router.uptime_hours:.1f}h"


def freshly_rebooted(routers):
    return [r.name for r in routers if r.is_fresh]


if __name__ == "__main__":
    fleet = [Router("edge-1", 0, 9000), Router("edge-2", 5000, 6000)]
    for r in fleet:
        print(status_line(r))
