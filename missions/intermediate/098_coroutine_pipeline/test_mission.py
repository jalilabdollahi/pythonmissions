import pytest, asyncio, sys
sys.path.insert(0, ".")
from broken import pipeline_process

def test_pipeline():
    result = asyncio.run(pipeline_process(
        [1, 2, 3],
        [lambda x: x * 2, lambda x: x + 1]
    ))
    assert result == [3, 5, 7]

def test_empty_pipeline():
    result = asyncio.run(pipeline_process([5, 6], []))
    assert result == [5, 6]
