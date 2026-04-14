import pytest, sys
sys.path.insert(0, ".")
from broken import sanitize_job_name, push_metrics
from unittest.mock import MagicMock

def test_sanitize():
    assert sanitize_job_name("batch job") == "batch_job"
    assert sanitize_job_name("nightly-run") == "nightly_run"

def test_push_url():
    sess = MagicMock()
    resp = MagicMock()
    resp.status_code = 200
    sess.post.return_value = resp
    push_metrics(sess, "http://pushgw:9091", "batch_job", "# metrics\n")
    url = sess.post.call_args[0][0]
    assert "/metrics/job/batch_job" in url
