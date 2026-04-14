# Mission 134 - Solution
def format_alert(level, msg):
    return "[{level}] {msg}".format(level=level, msg=msg)

if __name__ == "__main__":
    print(format_alert("CRITICAL", "Disk full on web-01"))
