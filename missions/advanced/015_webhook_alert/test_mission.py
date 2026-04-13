import json
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(__file__))


def make_mock_response(status_code=200):
    m = MagicMock()
    m.status_code = status_code
    m.raise_for_status = MagicMock()
    return m


def test_send_alert_uses_json_not_form_data():
    from broken import send_alert

    with patch("broken.requests.post", return_value=make_mock_response()) as mock_post:
        send_alert("http://hook.example.com", "Test", "Message")
        call_kwargs = mock_post.call_args[1]

        if "data" in call_kwargs:
            data_val = call_kwargs["data"]
            assert not isinstance(data_val, dict)

        uses_json_kwarg = "json" in call_kwargs
        uses_data_string = "data" in call_kwargs and isinstance(call_kwargs["data"], str)
        assert uses_json_kwarg or uses_data_string


def test_send_alert_json_content_type_when_using_data_string():
    from broken import send_alert

    with patch("broken.requests.post", return_value=make_mock_response()) as mock_post:
        send_alert("http://hook.example.com", "Test", "Message")
        call_kwargs = mock_post.call_args[1]

        if "data" in call_kwargs and isinstance(call_kwargs["data"], str):
            headers = call_kwargs.get("headers", {})
            ct = headers.get("Content-Type", "")
            assert "application/json" in ct


def test_send_alert_payload_is_valid_json():
    from broken import send_alert
    received_body = {}

    def capture_post(url, **kwargs):
        if "json" in kwargs:
            received_body.update(kwargs["json"])
        elif "data" in kwargs and isinstance(kwargs["data"], str):
            received_body.update(json.loads(kwargs["data"]))
        return make_mock_response()

    with patch("broken.requests.post", side_effect=capture_post):
        send_alert("http://hook.example.com", "Test Title", "Test body")

    assert "text" in received_body
    assert "Test Title" in received_body["text"]


def test_send_alert_returns_status_code():
    from broken import send_alert
    with patch("broken.requests.post", return_value=make_mock_response(200)):
        result = send_alert("http://hook.example.com", "T", "B")
    assert result == 200


def test_send_deploy_alert_calls_send_alert():
    from broken import send_deploy_alert
    with patch("broken.requests.post", return_value=make_mock_response(200)):
        result = send_deploy_alert("http://hook.example.com", "svc", "1.0.0", "prod", "ali")
    assert result == 200


def test_send_incident_alert_severity_critical():
    from broken import send_incident_alert
    captured = {}

    def capture(url, **kwargs):
        body = kwargs.get("json") or json.loads(kwargs.get("data", "{}"))
        captured.update(body)
        return make_mock_response()

    with patch("broken.requests.post", side_effect=capture):
        send_incident_alert("http://hook.example.com", "db", "connection refused")

    attachments = captured.get("attachments", [{}])
    assert attachments[0].get("color") == "#cc0000"
