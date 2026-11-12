# Mission 298 - Pipeline Notation (solution)
# Tokenize and parse "build -> test & lint -> deploy" into ordered stages of parallel jobs.
import re


class ParseError(Exception):
    def __init__(self, message, pos):
        super().__init__(f"{message} at position {pos}")
        self.message = message
        self.pos = pos


TOKEN = re.compile(r"(?P<arrow>->)|(?P<amp>&)|(?P<name>[A-Za-z_]\w*(?:-\w+)*)")


def tokenize(text):
    """Return (kind, value, pos) tuples. Positions are 0-based character offsets."""
    tokens = []
    pos = 0
    while pos < len(text):
        if text[pos].isspace():
            pos += 1
            continue
        match = TOKEN.match(text, pos)
        if not match:
            raise ParseError(f"unexpected character {text[pos]!r}", pos)
        tokens.append((match.lastgroup, match.group(), pos))
        pos = match.end()
    return tokens


def parse(text):
    """stages := stage ('->' stage)* ; stage := job ('&' job)* ; job names are unique."""
    tokens = tokenize(text)
    stages, seen = [], set()
    i = 0
    while True:
        stage = []
        while True:
            if i >= len(tokens) or tokens[i][0] != "name":
                where = tokens[i][2] if i < len(tokens) else len(text)
                raise ParseError("expected a job name", where)
            name, pos = tokens[i][1], tokens[i][2]
            if name in seen:
                raise ParseError(f"duplicate job {name!r}", pos)
            seen.add(name)
            stage.append(name)
            i += 1
            if i < len(tokens) and tokens[i][0] == "amp":
                i += 1
                continue
            break
        stages.append(stage)
        if i >= len(tokens):
            return stages
        if tokens[i][0] != "arrow":
            raise ParseError("expected '->' or '&'", tokens[i][2])
        i += 1


def render(stages):
    return " -> ".join(" & ".join(stage) for stage in stages)


def run_order(stages):
    """Flatten into a (stage_index, job) list, as a scheduler would dispatch it."""
    return [(index, job) for index, stage in enumerate(stages) for job in stage]


def max_parallelism(stages):
    return max(len(stage) for stage in stages)
