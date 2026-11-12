# Mission 118 - Quiet Disk Monitor (solution)
# Logs disk usage readings at appropriate severity levels.
import logging

logger = logging.getLogger("pinecrest.disk")
logger.setLevel(logging.INFO)

WARN_AT = 80
ERROR_AT = 95


def check_disk(host, percent):
    if percent >= ERROR_AT:
        logger.error("%s disk at %d%%, nearly full", host, percent)
        return "ERROR"
    if percent >= WARN_AT:
        logger.warning("%s disk at %d%%, filling up", host, percent)
        return "WARNING"
    logger.info("%s disk at %d%%, healthy", host, percent)
    return "INFO"


def check_all(readings):
    flagged = []
    for host, percent in readings.items():
        if check_disk(host, percent) != "INFO":
            flagged.append(host)
    return flagged


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s %(message)s")
    print(check_all({"db-1": 97, "web-1": 85, "web-2": 20}))
