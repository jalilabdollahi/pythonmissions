#!/usr/bin/env python3
"""Validate PythonMissions content.

Checks every mission (or a subset with --only) for:
  * directory layout and catalog match
  * mission.yaml schema
  * broken.py FAILS its tests and solution.py PASSES them
  * test count and runtime
  * code similarity against every other mission (no two missions alike)

Usage:
  python tools/validate_missions.py                 # everything
  python tools/validate_missions.py --only 001-025  # a range (comma separated list allowed)
  python tools/validate_missions.py --no-tests      # schema + similarity only
"""

from __future__ import annotations

import argparse
import ast
import io
import itertools
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tokenize
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MISSIONS = ROOT / "missions"
CATALOG = ROOT / "tools" / "mission_catalog.txt"

LEVELS = {
    "beginner": (1, 120, 100, (1, 2)),
    "intermediate": (121, 220, 200, (2, 4)),
    "advanced": (221, 300, 300, (4, 5)),
}
REQUIRED_FILES = {"mission.yaml", "broken.py", "solution.py", "test_mission.py"}
IGNORED = {"__pycache__", ".pytest_cache"}
SIMILARITY_ERROR = 0.55
SIMILARITY_WARN = 0.40
TEST_TIMEOUT = 30


def load_catalog() -> dict[int, tuple[str, str]]:
    entries = {}
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\d{3} \|", line):
            continue
        num, slug, category, _ = [p.strip() for p in line.split("|", 3)]
        entries[int(num)] = (slug, category)
    return entries


def parse_only(spec: str | None) -> set[int] | None:
    if not spec:
        return None
    wanted: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            wanted.update(range(int(a), int(b) + 1))
        elif part:
            wanted.add(int(part))
    return wanted


def discover() -> list[Path]:
    dirs = []
    for level in LEVELS:
        level_dir = MISSIONS / level
        if level_dir.exists():
            dirs.extend(d for d in level_dir.iterdir() if d.is_dir() and d.name not in IGNORED)
    return sorted(dirs, key=lambda d: d.name)


def number_of(d: Path) -> int:
    m = re.match(r"^(\d{3})_", d.name)
    return int(m.group(1)) if m else -1


# ---------------------------------------------------------------- schema

def check_schema(d: Path, catalog) -> tuple[list[str], dict]:
    errors: list[str] = []
    num = number_of(d)
    level = d.parent.name
    lo, hi, xp, (dmin, dmax) = LEVELS[level]
    if num < 0:
        return [f"directory name must start with NNN_: {d.name}"], {}
    if not lo <= num <= hi:
        errors.append(f"number {num:03d} does not belong in {level} ({lo:03d}-{hi:03d})")
    if num in catalog:
        slug, _cat = catalog[num]
        if d.name != f"{num:03d}_{slug}":
            errors.append(f"directory should be {num:03d}_{slug}")
    else:
        errors.append("number not in catalog")

    present = {p.name for p in d.iterdir() if p.name not in IGNORED}
    missing = REQUIRED_FILES - present
    extra = present - REQUIRED_FILES
    if missing:
        errors.append(f"missing files: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected files: {sorted(extra)}")
    if missing:
        return errors, {}

    try:
        data = yaml.safe_load((d / "mission.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return errors + [f"mission.yaml does not parse: {exc}".splitlines()[0]], {}
    if not isinstance(data, dict):
        return errors + ["mission.yaml is not a mapping"], {}

    for key in ("title", "category", "story", "description", "lesson"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"mission.yaml: '{key}' missing or empty")
    if data.get("xp") != xp:
        errors.append(f"mission.yaml: xp must be {xp}")
    diff = data.get("difficulty")
    if not isinstance(diff, int) or not dmin <= diff <= dmax:
        errors.append(f"mission.yaml: difficulty must be {dmin}-{dmax}")
    hints = data.get("hints")
    if not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(h, str) and h.strip() for h in hints):
        errors.append("mission.yaml: exactly 3 non-empty string hints required")
    mistakes = data.get("mistakes")
    if not isinstance(mistakes, list) or not 2 <= len(mistakes) <= 3 or not all(isinstance(m, str) for m in mistakes):
        errors.append("mission.yaml: 'mistakes' must be a list of 2-3 strings")
    tags = data.get("tags")
    if not isinstance(tags, list) or not tags:
        errors.append("mission.yaml: 'tags' must be a non-empty list")
    if "description" in data and isinstance(data["description"], str) and "bug" not in data["description"].lower():
        errors.append("mission.yaml: description should state how many bugs there are")

    broken = (d / "broken.py").read_text(encoding="utf-8")
    solution = (d / "solution.py").read_text(encoding="utf-8")
    if not broken.startswith(f"# Mission {num:03d}"):
        errors.append(f"broken.py must start with '# Mission {num:03d} - ...'")
    if broken == solution:
        errors.append("broken.py and solution.py are identical")
    if re.search(r"#.*\b(BUG|FIXME|TODO: fix)\b", broken):
        errors.append("broken.py contains a comment that gives the bug away")
    try:
        tree = ast.parse((d / "test_mission.py").read_text(encoding="utf-8"))
        n_tests = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_"))
        if n_tests < 4:
            errors.append(f"test_mission.py has {n_tests} tests (need >= 4)")
    except SyntaxError as exc:
        errors.append(f"test_mission.py syntax error: {exc}")
    try:
        ast.parse(solution)
    except SyntaxError as exc:
        errors.append(f"solution.py syntax error: {exc}")
    return errors, data


# ---------------------------------------------------------------- tests

def run_suite(d: Path, source: str) -> tuple[int | str, float, str]:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / d.name
        work.mkdir()
        shutil.copy2(d / "test_mission.py", work / "test_mission.py")
        shutil.copy2(d / source, work / "broken.py")
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_mission.py"],
                cwd=work, capture_output=True, text=True, timeout=TEST_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return "timeout", TEST_TIMEOUT, ""
        return proc.returncode, time.perf_counter() - start, (proc.stdout + proc.stderr)


def check_tests(d: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    code, secs, out = run_suite(d, "solution.py")
    if code != 0:
        tail = "\n      ".join(out.strip().splitlines()[-6:])
        errors.append(f"solution.py does not pass (exit {code}):\n      {tail}")
    elif secs > 5:
        warnings.append(f"tests are slow ({secs:.1f}s)")
    code, _secs, out = run_suite(d, "broken.py")
    if code == 0:
        errors.append("broken.py passes all tests (no bug is detected)")
    elif code in (5, "timeout"):
        errors.append(f"broken.py run ended with {code} (must fail with test failures, not hang/no tests)")
    return errors, warnings


# ---------------------------------------------------------------- similarity

def shingles(path: Path, k: int = 5) -> set[tuple]:
    toks = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(path.read_text(encoding="utf-8")).readline):
            if tok.type in (tokenize.NAME, tokenize.OP):
                toks.append(tok.string)
            elif tok.type == tokenize.NUMBER:
                toks.append("0")
            elif tok.type == tokenize.STRING:
                toks.append("'s'")
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return set()
    return {tuple(toks[i:i + k]) for i in range(max(0, len(toks) - k + 1))}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="mission numbers, e.g. 001-025,030")
    ap.add_argument("--no-tests", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args()

    catalog = load_catalog()
    wanted = parse_only(args.only)
    all_dirs = discover()
    targets = [d for d in all_dirs if wanted is None or number_of(d) in wanted]

    errors: dict[str, list[str]] = {}
    warnings: dict[str, list[str]] = {}

    numbers = [number_of(d) for d in all_dirs]
    for n in {n for n in numbers if numbers.count(n) > 1}:
        errors.setdefault("global", []).append(f"duplicate mission number {n:03d}")

    metas = {}
    for d in targets:
        errs, data = check_schema(d, catalog)
        if errs:
            errors.setdefault(d.name, []).extend(errs)
        metas[d.name] = data

    # unique titles across the whole game
    titles: dict[str, str] = {}
    for d in all_dirs:
        try:
            data = metas.get(d.name) or yaml.safe_load((d / "mission.yaml").read_text(encoding="utf-8"))
            title = str(data.get("title", "")).strip().lower()
        except Exception:
            continue
        if title in titles and (d in targets or titles[title] in {t.name for t in targets}):
            errors.setdefault(d.name, []).append(f"title duplicates {titles[title]}")
        titles.setdefault(title, d.name)

    if not args.no_tests:
        runnable = [d for d in targets if not (REQUIRED_FILES - {p.name for p in d.iterdir()})]
        with ThreadPoolExecutor(args.jobs) as ex:
            for d, (errs, warns) in zip(runnable, ex.map(check_tests, runnable)):
                if errs:
                    errors.setdefault(d.name, []).extend(errs)
                if warns:
                    warnings.setdefault(d.name, []).extend(warns)

    sh = {d.name: shingles(d / "solution.py") | shingles(d / "test_mission.py") for d in all_dirs if (d / "solution.py").exists()}
    target_names = {d.name for d in targets}
    for a, b in itertools.combinations(sorted(sh), 2):
        if a not in target_names and b not in target_names:
            continue
        score = jaccard(sh[a], sh[b])
        owner = b if b in target_names else a
        other = a if owner == b else b
        if score >= SIMILARITY_ERROR:
            errors.setdefault(owner, []).append(f"too similar to {other} ({score:.2f})")
        elif score >= SIMILARITY_WARN:
            warnings.setdefault(owner, []).append(f"somewhat similar to {other} ({score:.2f})")

    for name in sorted(set(errors) | set(warnings)):
        print(f"\n{name}")
        for e in errors.get(name, []):
            print(f"  ERROR {e}")
        for w in warnings.get(name, []):
            print(f"  warn  {w}")

    n_err = sum(len(v) for v in errors.values())
    n_warn = sum(len(v) for v in warnings.values())
    print(f"\nChecked {len(targets)} missions: {n_err} errors, {n_warn} warnings")
    if wanted is not None:
        found = {number_of(d) for d in targets}
        absent = sorted(n for n in wanted if n not in found and n in catalog)
        if absent:
            print(f"Not yet created: {', '.join(f'{n:03d}' for n in absent)}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
