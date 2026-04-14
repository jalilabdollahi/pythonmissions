import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_calls_correct_number():
    from broken import poll_service
    calls = []
    def check():
        calls.append(1)
        return False
    poll_service(check, 5)
    assert len(calls) == 5

def test_returns_true_on_success():
    from broken import poll_service
    def succeeds():
        return True
    assert poll_service(succeeds, 3) is True

def test_returns_false_on_all_fail():
    from broken import poll_service
    assert poll_service(lambda: False, 3) is False
