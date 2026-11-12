# Mission 194 - Structured Logging Shift
# A logging.Formatter that emits one JSON object per line, including extra fields.
import json
import logging

_STANDARD = set(logging.LogRecord("n", 0, "p", 0, "m", (), None).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.msg,
            "ts": record.created,
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD:
                payload[key] = value
        return json.dumps(payload, sort_keys=True)


def make_logger(name, stream):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger.handlers[:] = [handler]
    return logger


def main():
    import sys

    logger = make_logger("demo", sys.stdout)
    logger.info("deploy %s finished", "v42", extra={"duration_s": 12.5})
    try:
        {}["missing"]
    except KeyError:
        logger.exception("lookup failed")


if __name__ == "__main__":
    main()
