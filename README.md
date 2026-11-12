# PythonMissions 🐍⚔️

![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-blue)
![python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![missions](https://img.shields.io/badge/missions-300-brightgreen)
![tests](https://img.shields.io/badge/mission%20tests-2%2C080-orange)

> **Learn Python for DevOps by fixing broken scripts.**

PythonMissions is a fully local, game-based Python troubleshooting platform with a terminal UI.
Each mission drops you into a realistic broken script: a deploy gate, a log parser, a token
bucket, a Raft vote handler, a CD orchestrator. You read the story, find the bugs, fix them in
a sandbox, and prove your work with tests.

**300 unique missions in 3 difficulty bands, from Python basics to distributed-systems internals.**
No cloud. No network. No lab costs. Just code, tests, and practice.

---

## ✨ Features

- 🐍 **300 missions**, each built around a different concept, with its own story, system and code. No two are alike, and a similarity checker enforces it.
- 🧪 **2,080 mission tests.** Every fix is checked by pytest, and each planted bug is caught by at least one test.
- 🧰 **Per-mission sandbox.** You edit `sandbox/<mission>/broken.py`. Your edits survive quitting, the tests are refreshed before every check, and the solution is never copied into the sandbox.
- 💡 **Three progressive hints** per mission, from a nudge to almost the answer.
- 📖 **Debrief after every mission**, with a lesson on the concept and its common mistakes.
- 🏆 **XP and 7 ranks**, from Intern to Distinguished Engineer.
- 🗺️ **Mission browser** to replay or jump to any mission.
- 💾 **Persistent progress** in `~/.pythonmissions/progress.json`.

---

## 🚀 Quick Start

```bash
cd pythonmissions
./install.sh     # creates ./venv (rebuilds it if broken) and installs deps
./play.sh
```

| Command | What it does |
|---------|--------------|
| `./play.sh` | Start or continue the campaign |
| `./play.sh --reset` | Wipe progress and sandbox edits |
| `./play.sh --validate` | Check every mission: the solution passes, the broken file fails, and no two missions are similar |
| `./play.sh --validate --only 221-240` | Check a range of missions |

### Requirements

| Tool | Notes |
|------|-------|
| Python **3.10+** | `brew install python` on macOS. Use `PYTHON=/path/to/python3 ./install.sh` to pick a specific interpreter. |
| A terminal editor | `$VISUAL` / `$EDITOR` (for example `code --wait`), otherwise `nano`, `vim` or `vi` |
| System time-zone data | Used by a few date/time missions. Present on macOS and on most Linux distros (`tzdata`). |

Dependencies: `rich`, `pyyaml`, `pytest`. Missions use only the standard library.

---

## 🎮 How to Play

1. Run `./play.sh` and enter your name the first time.
2. The campaign opens the first unfinished mission. Read the **story** and the **mission brief**. The brief describes what the code should do and how many bugs it has.
3. Press **E** to open `broken.py` in your editor, or open the path shown on screen in any IDE.
4. Press **Enter** to run the tests. Failing tests show what is still wrong.
5. When everything passes you earn XP, read the debrief, and move to the next mission.

### In-Game Keys

| Key | Action |
|-----|--------|
| `Enter` | Check your fix (runs the tests) |
| `E` | Open `broken.py` in your editor |
| `H` | Reveal the next hint |
| `R` | Restore the original broken file |
| `M` | Mission browser (`n`/`p` page, `b`/`i`/`a` jump to a level, type a number to play) |
| `P` | Progress overview |
| `S` | Show the solution (recorded in your progress) |
| `N` | Next mission (after completing the current one) |
| `Q` | Quit (Ctrl+C also quits safely) |

---

## 🗺️ Learning Path: 300 Missions · 56,000 XP

| Level | Missions | XP each | Bugs per mission | Topics |
|-------|----------|---------|------------------|--------|
| 🟢 Beginner | 001–120 | 100 | 1–2 | Strings, numbers, lists, dicts, sets, loops, logic, functions, files and paths, CSV/JSON, errors, classes, dates, bytes and hashing, networking basics, regex, CLI, logging |
| 🟡 Intermediate | 121–220 | 200 | 2–3 | Log parsing, config loading and merging, metrics and percentiles, alerting, caching, decorators, context managers, generators, subprocess, archives, security (HMAC, masking), HTTP, resilience (retry, circuit breaker, token bucket), threads, asyncio, sqlite, XML, struct |
| 🔴 Advanced | 221–300 | 300 | 3–4 | Consistent hashing, Raft voting, vector clocks, CRDTs, Merkle trees, Bloom filters, 2PC and sagas, event sourcing, WAL and LSM storage, MVCC, connection pools, async cancellation, lock ordering, load balancing, autoscaling, canary analysis, SLO burn rates, tracing, IaC reconcile loops, RBAC, AST tools, metaclasses, descriptors, chaos engineering, and a capstone CD orchestrator |

### Ranks

| XP | Rank |
|----|------|
| 0 | Intern |
| 1,000 | Junior DevOps |
| 3,000 | DevOps Engineer |
| 8,000 | Senior DevOps |
| 16,000 | Staff Engineer |
| 28,000 | Principal Engineer |
| 45,000 | Distinguished Engineer |

The concept behind every mission is listed in [`tools/mission_catalog.txt`](tools/mission_catalog.txt).

---

## 📁 Project Structure

```text
pythonmissions/
├── main.py                  # entry point
├── install.sh               # creates/repairs ./venv and installs deps
├── play.sh                  # launcher (--reset, --validate)
├── requirements.txt
├── engine/
│   ├── missions.py          # loads mission.yaml (a bad file is skipped, never fatal)
│   ├── progress.py          # XP, ranks, saved progress (atomic writes)
│   ├── runner.py            # editor launch + pytest runner with timeout
│   ├── sandbox.py           # per-mission editable copies
│   └── ui.py                # Rich terminal UI
├── missions/
│   ├── beginner/            # 001_hello_devops … 120_shlex_split
│   ├── intermediate/        # 121_nginx_log_named_groups … 220_binary_header_struct
│   └── advanced/            # 221_consistent_hash_ring … 300_cd_orchestrator
├── tests/
│   └── test_engine.py       # engine tests
├── tools/
│   ├── MISSION_SPEC.md      # how to write a mission
│   ├── mission_catalog.txt  # one unique concept per mission
│   └── validate_missions.py # content validator
└── sandbox/                 # your edits (git-ignored)
```

Each mission directory contains:

| File | Purpose |
|------|---------|
| `mission.yaml` | Title, story, brief, 3 hints, lesson, common mistakes |
| `broken.py` | The buggy script you fix |
| `solution.py` | The reference fix (the smallest change that works) |
| `test_mission.py` | The tests your fix must pass |

---

## 🛠️ Contributing Missions

1. Pick an unused concept, or add a new line to `tools/mission_catalog.txt`.
2. Follow [`tools/MISSION_SPEC.md`](tools/MISSION_SPEC.md).
3. Run `./play.sh --validate --only <NNN>`. It must report **0 errors**.

Engine tests:

```bash
./venv/bin/python -m pytest tests
```

---

## 🔄 Upgrading from the 15-mission version

The missions were rewritten from scratch, and their ids changed. On first launch, an old progress file is migrated: your player name is kept and XP starts from zero.

---

## 📄 License

MIT License.
