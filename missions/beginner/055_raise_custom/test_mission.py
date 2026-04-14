import os, sys, pytest
sys.path.insert(0, os.path.dirname(__file__))

def test_valid_port():
    from broken import validate_port
    assert validate_port(8080) == 8080

def test_raises_value_error():
    from broken import validate_port
    with pytest.raises(ValueError):
        validate_port(99999)

def test_zero_invalid():
    from broken import validate_port
    with pytest.raises(ValueError):
        validate_port(0)
