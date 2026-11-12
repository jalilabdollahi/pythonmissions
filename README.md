# PythonMissions 🐍⚔️

![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-blue)
![python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![missions](https://img.shields.io/badge/missions-300-brightgreen)

> **Learn Python for DevOps by fixing broken scripts.**

PythonMissions is a fully local, game-based Python troubleshooting platform with a terminal UI.
Each mission drops you into a realistic broken script: a config loader, a log parser, a
rate limiter, a deployment orchestrator. You diagnose the problem, fix it in a sandbox, and
prove your work with tests.

**300 unique missions across 3 difficulty bands, from Python basics to distributed-systems internals.**
No cloud. No network. No lab costs. Just code, tests, and practice.

---

## ✨ Features

- 🐍 **300 missions**, each built around a different concept. No two are alike.
- 🧪 **Test-driven validation.** Every fix is checked with mission-specific pytest tests.
- 🧰 **Per-mission sandbox.** You edit `sandbox/<mission>/broken.py`. Your edits survive quitting, and the real mission files stay untouched.
- 💡 **Three progressive hints** per mission.
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
| `./play.sh --validate` | Check every mission (solution passes, broken fails) |

Requirements: **Python 3.10+** and a terminal editor (`$VISUAL`/`$EDITOR`, `nano`, `vim`, or `code --wait`).

---

## 🎯 In-Game Keys

| Key | Action |
|-----|--------|
| `Enter` | Check your fix (runs the tests) |
| `E` | Open `broken.py` in your editor |
| `H` | Reveal the next hint |
| `R` | Restore the original broken file |
| `M` | Mission browser (replay or jump) |
| `P` | Progress overview |
| `S` | Show the solution (recorded) |
| `N` | Next mission (after completing the current one) |
| `Q` | Quit |

You can also edit the file in any IDE. The path is shown on the mission screen.

---

## 🗺️ Learning Path: 300 Missions · 56,000 XP

| Level | Missions | XP each | Focus |
|-------|----------|---------|-------|
| 🟢 Beginner | 001–120 | 100 | Types, strings, collections, loops, functions, files, classes, dates, CLI basics |
| 🟡 Intermediate | 121–220 | 200 | Parsing, config, metrics, caching, decorators, generators, subprocess, archives, security, threads, asyncio, sqlite |
| 🔴 Advanced | 221–300 | 300 | Distributed systems, CRDTs, storage engines, async pools, load balancing, deployments, observability, IaC, metaprogramming |

Ranks: Intern (0) → Junior DevOps (1,000) → DevOps Engineer (3,000) → Senior DevOps (8,000) →
Staff Engineer (16,000) → Principal Engineer (28,000) → Distinguished Engineer (45,000).

The full list of mission concepts is in [`tools/mission_catalog.txt`](tools/mission_catalog.txt).

---

## 📁 Project Structure

```text
pythonmissions/
├── main.py                  # entry point
├── install.sh / play.sh     # launcher scripts
├── engine/
│   ├── missions.py          # loads mission.yaml (bad files are skipped, not fatal)
│   ├── progress.py          # XP, ranks, saved progress
│   ├── runner.py            # editor + pytest runner
│   ├── sandbox.py           # per-mission editable copies
│   └── ui.py                # Rich terminal UI
├── missions/
│   ├── beginner/001_…120_…
│   ├── intermediate/121_…220_…
│   └── advanced/221_…300_…
├── tests/test_engine.py     # engine tests
├── tools/
│   ├── MISSION_SPEC.md      # how to write a mission
│   ├── mission_catalog.txt  # one unique concept per mission
│   └── validate_missions.py # content validator
└── sandbox/                 # your edits (git-ignored)
```

Each mission directory contains:

- `mission.yaml`: title, story, brief, 3 hints, lesson, common mistakes
- `broken.py`: the buggy script you fix
- `solution.py`: the reference fix
- `test_mission.py`: the tests your fix must pass

---

## 🛠️ Contributing Missions

1. Pick an unused concept, or add one to `tools/mission_catalog.txt`.
2. Follow `tools/MISSION_SPEC.md`.
3. Run `./play.sh --validate --only <NNN>`. It must report 0 errors.

Run the engine tests with `./venv/bin/python -m pytest tests`.

---

## 📄 License

MIT License.
