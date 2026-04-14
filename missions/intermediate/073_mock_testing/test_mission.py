import pytest, sys
sys.path.insert(0, ".")
from unittest.mock import patch, MagicMock
from broken import notify_slack, notify_team

def test_notify_slack_success():
    with patch("broken.requests.post") as mock_post:  # patch where used
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp
        result = notify_slack("http://hooks.slack.com/xxx", "hello")
        assert result is True
        assert mock_post.call_count == 1  # call_count not called_times

def test_notify_team():
    with patch("broken.requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp
        results = notify_team("http://hooks.slack.com/xxx", ["msg1", "msg2"])
        assert len(results) == 2
        assert mock_post.call_count == 2
