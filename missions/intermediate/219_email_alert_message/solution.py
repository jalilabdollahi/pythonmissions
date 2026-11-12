# Mission 219 - Alert Mail Builder (solution)
# Build alert emails and work out who the relay must deliver them to.
from email.message import EmailMessage
from email.utils import format_datetime, getaddresses

SENDER = "alerts@harbor.example"


def build_alert(subject, body, to, cc=(), date=None):
    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    msg["Subject"] = subject
    if date is not None:
        msg["Date"] = format_datetime(date)
    msg.set_content(body)
    return msg


def mark_urgent(msg):
    msg.replace_header("Subject", "[URGENT] " + msg["Subject"])
    msg["X-Priority"] = "1"
    return msg


def envelope_recipients(msg):
    pairs = getaddresses(msg.get_all("To", []) + msg.get_all("Cc", []))
    return sorted({address for _, address in pairs if address})


def add_html(msg, html_body):
    msg.add_alternative(html_body, subtype="html")
    return msg


def describe(msg):
    kinds = [part.get_content_type() for part in msg.walk()]
    return f"{msg['Subject']} -> {len(envelope_recipients(msg))} recipient(s), parts: {', '.join(kinds)}"


if __name__ == "__main__":
    mail = build_alert("disk full", "db1 is at 98%", ["a@x.example", "b@x.example"])
    print(describe(mail))
