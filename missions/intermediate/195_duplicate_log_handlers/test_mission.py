import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import io
import itertools
import logging

_ids = itertools.count()


def fresh(prefix="job"):
    return "%s-%d" % (prefix, next(_ids))


def test_single_setup_logs_each_line_once():
    out = io.StringIO()
    logger = broken.setup_logging(fresh(), out)
    logger.info("started")
    assert out.getvalue() == "INFO started\n"


def test_repeated_setup_does_not_duplicate_lines():
    app = fresh()
    out = io.StringIO()
    for _ in range(3):
        logger = broken.setup_logging(app, out)
    logger.info("tick")
    assert out.getvalue().splitlines() == ["INFO tick"], "calling setup again must not add another handler"
    assert len(logger.handlers) == 1


def test_error_stream_only_receives_errors():
    app = fresh()
    main, errs = io.StringIO(), io.StringIO()
    logger = broken.setup_logging(app, main, error_stream=errs)
    logger.info("fine")
    logger.error("boom")
    assert main.getvalue().splitlines() == ["INFO fine", "ERROR boom"]
    assert errs.getvalue().splitlines() == ["ERROR boom"]


def test_child_logger_prints_once_through_the_parent():
    app = fresh()
    out = io.StringIO()
    broken.setup_logging(app, out)
    child = broken.get_child(app, "db")
    child.info("query ok")
    assert out.getvalue().splitlines() == ["INFO query ok"], "children propagate to the parent's handler"
    assert child.handlers == []


class Tracking(logging.Handler):
    closed = False

    def emit(self, record):
        pass

    def close(self):
        self.closed = True
        super().close()


def test_close_logging_removes_every_handler():
    app = fresh()
    logger = broken.setup_logging(app, io.StringIO(), error_stream=io.StringIO())
    assert len(logger.handlers) == 2
    broken.close_logging(app)
    assert logger.handlers == [], "iterate over a copy of the handler list while removing"


def test_close_logging_closes_handlers_to_release_resources():
    app = fresh()
    logger = broken.setup_logging(app, io.StringIO())
    extra = Tracking()
    logger.addHandler(extra)
    broken.close_logging(app)
    assert extra.closed, "removing a handler is not enough, it must be closed too (files, sockets)"


def test_setup_after_close_starts_clean():
    app = fresh()
    broken.setup_logging(app, io.StringIO())
    broken.close_logging(app)
    out = io.StringIO()
    logger = broken.setup_logging(app, out)
    logger.warning("again")
    assert out.getvalue() == "WARNING again\n"
