# Mission 113 - Replica Name Extractor (solution)
# Pulls database host names and port numbers out of free-form incident notes.
import re

HOST_PATTERN = r"\bdb-[0-9]+\b"
PORT_PATTERN = r"\bport=([0-9]+)"


def find_hosts(text):
    return re.findall(HOST_PATTERN, text)


def find_ports(text):
    return [int(number) for number in re.findall(PORT_PATTERN, text)]


def summarize(text):
    return f"{len(find_hosts(text))} hosts, {len(find_ports(text))} ports"


def mentions_default_port(text):
    return 5432 in find_ports(text)


if __name__ == "__main__":
    note = "failover from db-12 to db-7, both on port=5432"
    print(summarize(note))
