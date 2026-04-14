import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_masks_correctly():
    from broken import mask_secret
    assert mask_secret("mysupersecrettoken") == "**************oken"

def test_last_four_visible():
    from broken import mask_secret
    result = mask_secret("abcdefgh")
    assert result.endswith("efgh")

def test_stars_count():
    from broken import mask_secret
    result = mask_secret("abcdefgh")
    assert result.count("*") == 4

def test_total_length_preserved():
    from broken import mask_secret
    s = "my-secret-key-xyz"
    assert len(mask_secret(s)) == len(s)
