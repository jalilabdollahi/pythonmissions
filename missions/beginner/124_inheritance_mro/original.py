# Mission 124 - Initialize the Logger Chain
class Logger:
    def __init__(self, level, fmt):
        self.level = level
        self.fmt = fmt

class FileLogger(Logger):
    def __init__(self, path, level, fmt):
        super().__init__(fmt, level)
        self.path = path

if __name__ == "__main__":
    fl = FileLogger("/var/log/app.log", "INFO", "%(msg)s")
    print(fl.level, fl.fmt)
