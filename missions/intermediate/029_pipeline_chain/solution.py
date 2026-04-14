# Mission 029 - Data Pipeline Chain
# Fixed solution
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
    return process(text)

def count_words(text):
    words = run_pipeline(text)
    return len(words)
