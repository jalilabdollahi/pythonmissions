# Mission 029 - Data Pipeline Chain
# Fix the 2 bugs in this script.
from functools import reduce

def pipeline(*funcs):
    """Create a pipeline that applies functions left to right."""
    def apply(data):
        return reduce(lambda acc, f: f(acc), funcs, data)
    return apply

def normalize(text):
    return text.strip().lower()

def tokenize(text):
    return text.split()

def remove_stop_words(words):
    stops = {"the", "a", "an", "is", "it"}
    return [w for w in words if w not in stops]

process = pipeline(normalize, tokenize, remove_stop_words)

def run_pipeline(text):
    return process(text)  # BUG 1: actually this is fine, bug is below

def count_words(text):
    words = run_pipeline(text)
    # BUG 2: should return len(words) not len(text)
    return len(text)
