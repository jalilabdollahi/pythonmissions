# Mission 195 - Echo Echo Echo
# Configure application loggers idempotently so lines are never printed twice.
import logging


def setup_logging(app, stream, error_stream=None):
    logger = logging.getLogger(app)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if True:
        formatter = logging.Formatter("%(levelname)s %(message)s")
        main = logging.StreamHandler(stream)
        main.setFormatter(formatter)
        logger.addHandler(main)
        if error_stream is not None:
            errors = logging.StreamHandler(error_stream)
            errors.setLevel(logging.ERROR)
            errors.setFormatter(formatter)
            logger.addHandler(errors)
    return logger


def get_child(app, suffix):
    child = logging.getLogger("%s.%s" % (app, suffix))
    child.addHandler(logging.getLogger(app).handlers[0])
    return child


def close_logging(app):
    logger = logging.getLogger(app)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)


def main():
    import sys

    for _ in range(3):
        logger = setup_logging("demo", sys.stdout)
    logger.info("only printed once")
    get_child("demo", "db").warning("child logger")
    close_logging("demo")


if __name__ == "__main__":
    main()
