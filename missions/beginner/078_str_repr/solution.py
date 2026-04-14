# Mission 078 - Solution
class Alert:
    def __init__(self, level, message):
        self.level = level
        self.message = message

    def __str__(self):
        return f"[{self.level}] {self.message}"

if __name__ == "__main__":
    a = Alert("CRITICAL", "Disk full on web-01")
    print(a)
