# Mission 090 - Uptime Calculator Crash
# Uptime helpers for the stand-up status bot.

SECONDS_PER_DAY = 86400


class Machine:
    def __init__(self, name, boot_epoch):
        self.name = name
        self.boot_epoch = boot_epoch

    def uptime_seconds(self, now):
        return now - self.boot_epoch

    def uptime_days(now):
        return self.uptime_seconds(now) // SECONDS_PER_DAY

    def needs_reboot(self, now, limit_days):
        return self.uptime_days(now) >= limit_days

    def label():
        return f"{self.name} (booted {self.boot_epoch})"


def stand_up_lines(machines, now):
    return [f"{m.name}: {m.uptime_days(now)}d" for m in machines]


if __name__ == "__main__":
    fleet = [Machine("gw-1", 1_700_000_000), Machine("gw-2", 1_690_000_000)]
    print("\n".join(stand_up_lines(fleet, 1_700_500_000)))
