import os, sys, pytest
sys.path.insert(0, os.path.dirname(__file__))

def test_200_passes():
    from broken import assert_success
    assert_success(200)

def test_201_passes():
    from broken import assert_success
    assert_success(201)

def test_500_raises():
    from broken import assert_success
    with pytest.raises(AssertionError):
        assert_success(500)

def test_404_raises():
    from broken import assert_success
    with pytest.raises(AssertionError):
        assert_success(404)
