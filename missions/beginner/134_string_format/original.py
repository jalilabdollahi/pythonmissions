# Mission 134 - Format the Alert Message
def format_alert(level, msg):
    """Return formatted alert string."""
    return "[{level}] {message}".format(level=level, msg=msg)

if __name__ == "__main__":
    print(format_alert("CRITICAL", "Disk full on web-01"))
