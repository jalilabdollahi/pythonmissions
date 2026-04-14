import os, sys, pytest
sys.path.insert(0, os.path.dirname(__file__))

def test_raises_service_error():
    from broken import connect
    with pytest.raises(Exception) as exc_info:
        connect("db.internal")
    from broken import ServiceError
    assert isinstance(exc_info.value, ServiceError)

def test_cause_is_set():
    from broken import connect
    try:
        connect("db.internal")
    except Exception as e:
        assert e.__cause__ is not None
