import pytest, sys
sys.path.insert(0, ".")
from broken import lint_dockerfile

GOOD = """FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt && python setup.py install
"""

BAD = """FROM python:latest
RUN apt-get update
RUN apt-get install -y curl
"""

def test_good_dockerfile():
    issues = lint_dockerfile(GOOD)
    assert issues == []

def test_latest_tag():
    issues = lint_dockerfile(BAD)
    assert any("latest" in i for i in issues)

def test_multiple_run():
    issues = lint_dockerfile(BAD)
    assert any("combine RUN" in i for i in issues)
