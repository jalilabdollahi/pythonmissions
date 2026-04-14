import os, sys, pytest
sys.path.insert(0, os.path.dirname(__file__))

def test_cannot_instantiate_without_check():
    from broken import Monitor
    class Bad(Monitor):
        pass
    with pytest.raises(TypeError):
        Bad()

def test_can_instantiate_with_check():
    from broken import Monitor
    class Good(Monitor):
        def check(self):
            return "ok"
    g = Good()
    assert g.check() == "ok"
