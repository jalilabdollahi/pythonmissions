import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def metric(samples, name="jobs_total", kind="counter"):
    return {"name": name, "type": kind, "help": "Jobs processed.", "samples": samples}


def test_simple_metric_layout():
    text = broken.render_metrics([metric([({}, 5)])])
    assert text == "# HELP jobs_total Jobs processed.\n# TYPE jobs_total counter\njobs_total 5\n"


def test_output_ends_with_newline():
    text = broken.render_metrics([metric([({"a": "1"}, 1)])])
    assert text.endswith("\n"), "every line of the exposition format is newline terminated"
    assert not text.endswith("\n\n")


def test_labels_are_sorted_by_name():
    text = broken.render_metrics([metric([({"zone": "b", "app": "x", "env": "p"}, 2)])])
    assert 'jobs_total{app="x",env="p",zone="b"} 2' in text


def test_quote_in_label_value_is_escaped():
    assert broken.escape_label_value('say "hi"') == 'say \\"hi\\"'


def test_backslash_is_escaped_first():
    assert broken.escape_label_value("C:\\temp") == "C:\\\\temp"
    assert broken.escape_label_value('\\"') == '\\\\\\"'


def test_newline_is_escaped():
    assert broken.escape_label_value("a\nb") == "a\\nb"


def test_help_and_type_once_per_metric_and_integer_floats():
    m = metric([({"q": "1"}, 3.0), ({"q": "2"}, 4.5)], name="depth", kind="gauge")
    text = broken.render_metrics([m])
    assert text.count("# HELP depth") == 1
    assert text.count("# TYPE depth gauge") == 1
    assert 'depth{q="1"} 3\n' in text
    assert 'depth{q="2"} 4.5\n' in text
