# Mission authoring spec

Every mission is a small, realistic DevOps/backend Python script with planted bugs.
The player edits `broken.py` until `test_mission.py` passes.

## Directory

```
missions/<level>/<NNN>_<slug>/
    mission.yaml
    broken.py        # the buggy script the player edits
    solution.py      # broken.py with ONLY the bugs fixed
    test_mission.py  # pytest tests, import from `broken`
```

`NNN` and `slug` come from `tools/mission_catalog.txt`. Numbering is global:
001-120 `beginner`, 121-220 `intermediate`, 221-300 `advanced`.
Do not add any other files (no original.py, no data files: build fixtures inside tests with `tmp_path`).

## mission.yaml

```yaml
title: Short Catchy Title            # unique, 2-6 words
category: Strings                    # from the catalog line
difficulty: 2                        # beginner 1-2, intermediate 2-4, advanced 4-5
xp: 100                              # beginner 100, intermediate 200, advanced 300
story: |
  2-4 sentences. A concrete on-call / ops situation with a named fictional
  team or system. Every story must be different (no "first day on the job" twice).
description: |
  What the script is supposed to do (its contract), which functions exist,
  and "There are N bugs." Do NOT say how to fix them.
hints:
  - |
    Hint 1: points at the area / symptom.
  - |
    Hint 2: names the concept or stdlib tool.
  - |
    Hint 3: nearly gives the fix.
tags: [tag1, tag2, tag3]
lesson: |
  3-5 sentences teaching the concept behind the bug and why it matters in real ops work.
mistakes:
  - A common wrong fix or misconception.
  - Another one.
```

Rules: always use block scalars (`|`) for story/description/lesson/hints so quotes and
colons never break YAML. Exactly 3 hints. `mistakes` has 2-3 items (plain strings; quote them if they contain `: ` or start with a special char).

## broken.py

- Header comment: `# Mission NNN - <Title>` then a one-line purpose comment.
- Size: beginner 20-70 lines, intermediate 40-120, advanced 70-220.
- Bugs: beginner 1-2, intermediate 2-3, advanced 3-4. Bugs are realistic mistakes
  (logic, wrong API usage, edge cases), not typos. A syntax error is allowed in at most a
  couple of beginner missions in the whole game; avoid it.
- No comments that reveal a bug (`# BUG`, `# FIXME`, `# wrong`).
- Must be importable without side effects: put any CLI behaviour under `if __name__ == "__main__":`.
- Standard library only (plus `yaml` if truly useful). No network, no real sleeping
  (inject a clock/sleep function when time matters), no reading files outside `tmp_path`.
- Python 3.10 compatible (no `tomllib`, no `asyncio.TaskGroup`, no `except*`, no
  `datetime.fromisoformat("...Z")`).
- Each mission's code must be original: its own domain objects, function names and data.
  Do not reuse scenarios or helpers from other missions.

## solution.py

Identical to broken.py except: the header line reads `# Mission NNN - <Title> (solution)` and
the bugs are fixed with the smallest sensible change. No refactors.

## test_mission.py

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken  # or: from broken import x, y
```

- 4-10 test functions, descriptive names (`test_rejects_port_above_65535`).
- Every planted bug must make at least one test fail on its own: if you fix all bugs but one,
  the suite must still fail.
- Deterministic and fast (< 2 s for the whole file). Use `tmp_path`, `capsys`, `monkeypatch`,
  fake clocks, fake fetchers. For asyncio use `asyncio.run(...)` inside a normal test (no pytest-asyncio).
- Tests check behaviour, not implementation details (do not assert on source text).
- Use assertion messages or clear names so a failing test teaches the player something.

## Validation

```
<python> tools/validate_missions.py --only 001-025
```

It checks YAML schema, that `solution.py` passes and `broken.py` fails, timing,
and similarity with other missions. A batch is done only when it reports 0 errors.
