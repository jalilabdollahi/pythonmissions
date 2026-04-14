import pytest, sys, json
sys.path.insert(0, ".")
from broken import parse_tf_output, get_output_value

TF_OUTPUT = json.dumps({
    "vpc_id": {"value": "vpc-0abc123", "type": "string"},
    "instance_count": {"value": 3, "type": "number"},
    "endpoint": {"value": None, "type": "string"},
})

def test_parse_output():
    result = parse_tf_output(TF_OUTPUT)
    assert result["vpc_id"] == "vpc-0abc123"
    assert result["instance_count"] == 3

def test_null_value():
    result = parse_tf_output(TF_OUTPUT)
    assert result["endpoint"] is None

def test_get_output():
    val = get_output_value(TF_OUTPUT, "vpc_id")
    assert val == "vpc-0abc123"

def test_get_missing():
    assert get_output_value(TF_OUTPUT, "nonexistent") is None
