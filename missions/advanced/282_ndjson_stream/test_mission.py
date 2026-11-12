import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import batched, count_by, iter_records, new_stats, summarize


class CountingSource:
    def __init__(self, lines):
        self.lines = lines
        self.consumed = 0

    def __iter__(self):
        for line in self.lines:
            self.consumed += 1
            yield line


def test_valid_lines_become_records():
    stats = new_stats()
    out = list(iter_records(['{"a": 1}\n', '{"b": 2}\r\n'], stats))
    assert out == [{"a": 1}, {"b": 2}]
    assert stats["records"] == 2 and stats["malformed"] == 0


def test_stream_is_lazy():
    source = CountingSource(['{"n": %d}' % i for i in range(1000)])
    records = iter_records(source, new_stats())
    assert next(records) == {"n": 0}
    assert source.consumed == 1, "reading one record must not read the whole input"


def test_blank_lines_are_not_malformed():
    stats = new_stats()
    out = list(iter_records(['{"a": 1}', "", "   ", '{"a": 2}'], stats))
    assert len(out) == 2
    assert stats["blank"] == 2
    assert stats["malformed"] == 0


def test_non_object_json_is_malformed():
    stats = new_stats()
    out = list(iter_records(["[1, 2]", "42", '"text"', "null", '{"ok": true}'], stats))
    assert out == [{"ok": True}], "only JSON objects are records"
    assert stats["malformed"] == 4


def test_bad_line_numbers_are_one_based():
    stats = new_stats()
    list(iter_records(['{"a": 1}', "{broken", '{"a": 2}', "also bad"], stats))
    assert stats["bad_line_numbers"] == [2, 4]
    assert stats["lines"] == 4


def test_batched_keeps_the_partial_tail():
    assert list(batched(iter(range(5)), 2)) == [[0, 1], [2, 3], [4]]
    assert list(batched([], 3)) == []


def test_summarize_reads_a_file(tmp_path):
    path = tmp_path / "events.ndjson"
    rows = [{"level": "info"}, {"level": "error"}, {"level": "info"}, {"msg": "x"}]
    text = "\n".join(json.dumps(r) for r in rows) + "\nnot json\n\n"
    path.write_text(text)
    counts, stats = summarize(str(path), "level")
    assert counts == {"info": 2, "error": 1, "unknown": 1}
    assert stats["bad_line_numbers"] == [5]
    assert count_by([], "level") == {}
