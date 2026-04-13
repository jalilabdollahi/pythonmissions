# PythonMissions 🐍⚔️

![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20-blue)
![shell](https://img.shields.io/badge/shell-bash-brightgreen)
![python](https://img.shields.io/badge/python-learning-3776AB)

> **Learn Python for DevOps by fixing broken scripts.**

PythonMissions is a fully local, game-based Python troubleshooting platform with a terminal UI. Each mission drops you into a realistic broken script, asks you to diagnose the problem, fix it in a sandbox, and prove your work with tests.

**15 progressive missions across 3 difficulty bands — from basic Python syntax to concurrent DevOps tooling.**  
No cloud. No lab costs. Just code, tests, and practice.

---

## ✨ Features

- 🐍 **15 missions** across beginner, intermediate, and advanced levels
- 🧪 **Test-driven validation** — every fix is checked with mission-specific pytest tests
- 🧰 **Sandbox workflow** — players edit a safe copy under `sandbox/current`
- 💡 **Progressive hints** — reveal help only when needed
- 📖 **Post-level lessons** — debrief and common mistakes after a successful mission
- 🏆 **XP and rank progression** — move from Intern to Principal Engineer
- ▶️ **Game-style launcher** — `install.sh` and `play.sh` flow like the other missions projects
- 💾 **Persistent progress** — saved under `~/.pythonmissions/progress.json`

---

## 🚀 Quick Start

```bash
cd pythonmissions
./install.sh
./play.sh
```

If you already installed dependencies, you can launch directly with:

```bash
./play.sh
```

Reset progress:

```bash
./play.sh --reset
```

---

## 📋 Prerequisites

| Tool | Install |
|------|---------|
| Python **3.9+** | `brew install python@3.11` |
| pip / venv support | usually included with Python |
| A terminal editor | `nano`, `vim`, `vi`, or your `$EDITOR` |

---

## 🎮 How to Play

1. **Run** `./play.sh`
2. **Enter your name** the first time you launch the game
3. **Start at mission 1 automatically** — progression moves from easy to hard
4. **Press `E`** to open the mission file in your editor
5. **Fix the bug** in the sandbox copy
6. **Press Enter** to run `Check` and validate your solution
7. **Read the debrief** and move to the next level

The real mission source files stay untouched. The active editable copy is created under `sandbox/current/`.

---

## 🎯 In-Game Commands

| Key | Action |
|-----|--------|
| `Enter` | Check the current solution |
| `E` | Edit the current mission file |
| `H` | Show the next hint |
| `R` | Reset the sandbox copy to the original broken version |
| `P` | Show progress |
| `S` | Show the solution |
| `Q` | Quit the game |

---

## 🗺️ Learning Path — 15 Missions · 3 Levels · 3,000 XP

| Level | Missions | XP Each | Focus |
|-------|----------|---------|-------|
| 🟢 Beginner | 5 | 100 | Variables, env vars, file I/O, argparse, string formatting |
| 🟡 Intermediate | 5 | 200 | Regex, requests, JSON, subprocess, YAML |
| 🔴 Advanced | 5 | 300 | Decorators, concurrency, tailing logs, deploy logic, webhooks |

Ranks:

- `0 XP` → Intern
- `200 XP` → Junior DevOps
- `500 XP` → DevOps Engineer
- `1000 XP` → Senior DevOps
- `1500 XP` → Staff Engineer
- `2000 XP` → Principal Engineer

---

## 📁 Project Structure

```text
pythonmissions/
├── main.py
├── install.sh
├── setup.sh
├── play.sh
├── requirements.txt
├── engine/
│   ├── missions.py
│   ├── progress.py
│   ├── runner.py
│   ├── sandbox.py
│   └── ui.py
├── missions/
│   ├── beginner/
│   │   ├── 001_hello_devops/
│   │   ├── 002_env_secrets/
│   │   ├── 003_read_logfile/
│   │   ├── 004_parse_args/
│   │   └── 005_format_output/
│   ├── intermediate/
│   │   ├── 006_parse_logs/
│   │   ├── 007_health_check/
│   │   ├── 008_json_config/
│   │   ├── 009_run_commands/
│   │   └── 010_yaml_config/
│   └── advanced/
│       ├── 011_retry_logic/
│       ├── 012_bulk_requests/
│       ├── 013_tail_logs/
│       ├── 014_deploy_check/
│       └── 015_webhook_alert/
└── sandbox/
    └── current/              ← active editable mission copy
```

Each mission directory contains:

- `mission.yaml` — mission metadata, story, hints
- `broken.py` — intentionally broken source
- `original.py` — reset source
- `test_mission.py` — validation tests
- `solution.py` — reference solution

---

## 🔄 Resetting Progress

Reset from the launcher:

```bash
./play.sh --reset
```

Reset the active mission sandbox from inside the game with `R`.

---

## 🎓 After Each Level

When you solve a mission, PythonMissions:

- runs the tests
- awards XP
- shows a short debrief
- shows common mistakes
- then advances to the next mission

---

## 📄 License

MIT License.
