"""Main TUI - all screens and the game loop."""

from __future__ import annotations

import getpass
import time
from pathlib import Path
from typing import List, Optional

from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table

from .missions import LEVELS, Mission, load_missions
from .progress import Progress
from .runner import get_editor, open_editor, run_tests
from .sandbox import prepare_sandbox, refresh_tests, reset_sandbox

console = Console()

WORDMARK = r"""
██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ██╗███████╗
████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ██║██╔════╝
██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ██║███████╗
██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗██║╚════██║
██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚████║███████║
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
"""

LEVEL_STYLE = {"beginner": "bold green", "intermediate": "bold yellow", "advanced": "bold red"}
LEVEL_EMOJI = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}
LEVEL_BORDER = {"beginner": "green", "intermediate": "yellow", "advanced": "red"}
PAGE_SIZE = 20


class GameUI:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent
        self.missions: List[Mission] = []
        self.progress = Progress()
        self.sandbox: Optional[Path] = None

    # ------------------------------------------------------------ helpers

    @property
    def mission_ids(self) -> List[str]:
        return [m.id for m in self.missions]

    def _xp(self) -> int:
        return self.progress.total_xp(self.mission_ids)

    def _done(self) -> int:
        return self.progress.completed_count(self.mission_ids)

    def _pause(self, message: str = "Press Enter to continue") -> None:
        Prompt.ask(f"[dim]{message}[/dim]", default="", show_default=False)

    def _next_mission(self, after: Optional[Mission] = None) -> Optional[Mission]:
        """First unfinished mission, preferring ones after `after`."""
        if after is not None and after in self.missions:
            start = self.missions.index(after) + 1
            ordered = self.missions[start:] + self.missions[:start]
        else:
            ordered = self.missions
        return next((m for m in ordered if not self.progress.is_completed(m.id)), None)

    # ------------------------------------------------------------ main loop

    def run(self):
        self.missions, load_errors = load_missions(self.base_path)
        if load_errors:
            console.print("[yellow]Some missions could not be loaded and were skipped:[/yellow]")
            for err in load_errors:
                console.print(f"  [dim]- {escape(err)}[/dim]")
            self._pause()
        if not self.missions:
            console.print("[red]No missions found! Check the missions/ directory.[/red]")
            return

        self._ensure_player_name()

        mission = self._next_mission()
        while True:
            if mission is None:
                self._campaign_complete()
                mission = self._mission_browser()
                if mission is None:
                    break
            action = self._play_mission(mission)
            if action == "quit":
                break
            if isinstance(action, Mission):
                mission = action
            else:  # "advance"
                mission = self._next_mission(after=mission)
        self._goodbye()

    def _ensure_player_name(self):
        if self.progress.player_name():
            return
        self._print_header()
        console.print("[bold]WELCOME, OPERATOR[/bold]\n")
        console.print(
            f"{len(self.missions)} broken scripts are waiting. The campaign starts with the easiest one "
            "and gets harder as you go.\n"
        )
        try:
            default_name = getpass.getuser() or "DevOps Agent"
        except Exception:
            default_name = "DevOps Agent"
        name = Prompt.ask("[cyan]Your name[/cyan]", default=default_name).strip()
        self.progress.set_player_name(name or default_name)

    # ------------------------------------------------------------ chrome

    def _print_header(self, compact: bool = False):
        console.clear()
        if compact:
            console.print(Rule("[bold cyan]PYTHON MISSIONS[/bold cyan]  [dim]Python for DevOps[/dim]"))
        else:
            console.print()
            console.print(
                Panel(
                    f"[bold cyan]{WORDMARK}[/bold cyan]\n"
                    "[dim]Python for DevOps  ·  Fix Broken Scripts  ·  Level Up[/dim]",
                    border_style="cyan",
                    padding=(1, 2),
                )
            )
        console.print()

    def _print_xp_bar(self):
        xp = self._xp()
        done = self._done()
        total = len(self.missions)
        rank = self.progress.rank_for(xp)
        next_rank, xp_needed = self.progress.next_rank_for(xp)

        filled = int((done / total) * 24) if total else 0
        bar = "[green]" + "█" * filled + "[/green][dim]" + "░" * (24 - filled) + "[/dim]"
        name = escape(self.progress.player_name() or "Operator")
        line = f"[cyan]{name}[/cyan]  [bold]{rank}[/bold]  [cyan]XP[/cyan] [bold yellow]{xp:,}[/bold yellow]"
        if next_rank:
            line += f" [dim](+{xp_needed:,} to {next_rank})[/dim]"
        line += f"  {bar} [dim]{done}/{total}[/dim]"
        console.print(line)
        console.print()

    # ------------------------------------------------------------ mission screen

    def _play_mission(self, mission: Mission):
        self.sandbox = prepare_sandbox(self.base_path, mission.path)
        position = self.missions.index(mission) + 1

        while True:
            self._print_header(compact=True)
            self._print_xp_bar()
            style = LEVEL_STYLE[mission.level]
            done = self.progress.is_completed(mission.id)

            console.print(
                Panel(
                    f"[bold white]{escape(mission.title)}[/bold white]"
                    + ("  [bold green]✓ COMPLETE[/bold green]" if done else "")
                    + f"\n\n{escape(mission.story)}",
                    title=(
                        f"[{style}]{LEVEL_EMOJI[mission.level]} Mission {mission.number} · "
                        f"{mission.level.upper()} · {escape(mission.category)} · "
                        f"{mission.difficulty_stars} · {mission.xp} XP[/{style}]"
                    ),
                    subtitle=f"[dim]{position} of {len(self.missions)}[/dim]",
                    border_style=LEVEL_BORDER[mission.level],
                    padding=(1, 2),
                )
            )
            if mission.description:
                console.print(
                    Panel(escape(mission.description), title="[bold]Mission Brief[/bold]",
                          border_style="blue", padding=(0, 2))
                )
            console.print(f"[dim]Your file:[/dim] [bold]{escape(str(self.sandbox / 'broken.py'))}[/bold]")
            console.print()

            hints_left = len(mission.hints) - self.progress.hints_used(mission.id)
            has_solution = mission.solution_path.exists()
            items = [
                "[cyan][Enter][/cyan] Check",
                "[cyan][E][/cyan] Edit",
                f"[cyan][H][/cyan] Hint [dim]({hints_left})[/dim]",
                "[cyan][R][/cyan] Reset",
                "[cyan][M][/cyan] Missions",
                "[cyan][P][/cyan] Progress",
            ]
            if has_solution:
                items.append("[cyan][S][/cyan] Solution")
            if done:
                items.append("[cyan][N][/cyan] Next")
            items.append("[cyan][Q][/cyan] Quit")
            console.print("  " + "  ".join(items))
            console.print()

            choice = Prompt.ask("[dim]Action[/dim]", default="", show_default=False).strip().lower()

            if choice in ("", "t", "c"):
                if self._check(mission):
                    return "advance"
            elif choice == "e":
                self._edit()
            elif choice == "h":
                self._hint(mission)
            elif choice == "r":
                self._reset(mission)
            elif choice == "m":
                picked = self._mission_browser(current=mission)
                if picked is not None:
                    return picked
            elif choice == "p":
                self._show_progress()
            elif choice == "s" and has_solution:
                self._solution(mission)
            elif choice == "n" and done:
                return "advance"
            elif choice == "q":
                return "quit"

    def _edit(self):
        editor = get_editor()
        target = self.sandbox / "broken.py"
        console.print(f"\n[dim]Opening broken.py in {escape(editor)}... save and close it when done.[/dim]\n")
        time.sleep(0.5)
        ok, err = open_editor(target)
        if not ok:
            console.print(f"[red]Could not open editor: {escape(err)}[/red]")
            console.print("[dim]Edit this file in any editor, then press Enter here to check it:[/dim]")
            console.print(f"[bold]{escape(str(target))}[/bold]\n")
            self._pause()

    def _check(self, mission: Mission) -> bool:
        refresh_tests(self.sandbox, mission.path)
        self.progress.record_attempt(mission.id)
        console.print()
        with console.status("[cyan]Running tests...[/cyan]", spinner="dots"):
            passed, output, failed = run_tests(self.sandbox)

        if not passed:
            lines = []
            for line in output.splitlines():
                if line.startswith("==="):
                    # pytest section banners are padded with '=' to the terminal width
                    lines.append(f"[bold]{escape(line.strip('= '))}[/bold]")
                    continue
                text = escape(line.rstrip())
                if " PASSED" in line:
                    lines.append(f"[green]{text}[/green]")
                elif " FAILED" in line or " ERROR" in line or line.startswith(("E ", "FAILED", "ERROR")):
                    lines.append(f"[red]{text}[/red]")
                elif line.strip():
                    lines.append(f"[dim]{text}[/dim]")
            summary = f"{len(failed)} test(s) failing" if failed else "tests could not run"
            console.print(Panel("\n".join(lines[-60:]), title=f"[bold red]✗ {summary}[/bold red]",
                                border_style="red", padding=(1, 2)))
            hints_left = len(mission.hints) - self.progress.hints_used(mission.id)
            if hints_left > 0:
                console.print(f"[dim]Stuck? Press [H] for a hint ({hints_left} left).[/dim]")
            console.print()
            self._pause()
            return False

        passed_lines = [
            "✓ " + escape(l.split("::", 1)[-1].split(" PASSED")[0].strip())
            for l in output.splitlines() if " PASSED" in l
        ]
        console.print(Panel("[bold green]✓ ALL TESTS PASSED[/bold green]\n\n[dim]" + "\n".join(passed_lines) + "[/dim]",
                            border_style="green", padding=(1, 2)))
        before = self._xp()
        if self.progress.complete_mission(mission.id, mission.xp):
            after = self._xp()
            console.print(f"\n[bold yellow]🎉 +{mission.xp} XP[/bold yellow]  "
                          f"[dim]total {after:,}[/dim]")
            old_rank, new_rank = self.progress.rank_for(before), self.progress.rank_for(after)
            if new_rank != old_rank:
                console.print(f"[bold magenta]⬆ PROMOTED: {old_rank} → {new_rank}[/bold magenta]")
        self._show_lesson(mission)
        nxt = self._next_mission(after=mission)
        if nxt is not None:
            console.print(f"[bold cyan]Next mission:[/bold cyan] {nxt.number} · {escape(nxt.title)}")
        else:
            console.print("[bold cyan]That was the last open mission. Campaign complete![/bold cyan]")
        console.print()
        self._pause("Press Enter for the next mission")
        return True

    def _show_lesson(self, mission: Mission):
        lesson = mission.lesson or (
            f"This mission practised {escape(mission.category)}"
            + (f" ({', '.join(mission.tags[:4])})" if mission.tags else "")
            + ". Reproduce the failure, read the error, make the smallest correct change, prove it with tests."
        )
        console.print()
        console.print(Panel(escape(lesson), title="[bold green]📖 Debrief[/bold green]",
                            border_style="green", padding=(1, 2)))
        mistakes = mission.mistakes or [
            "Changing code before reading the failing test and traceback.",
            "Refactoring more than needed instead of making the smallest fix.",
        ]
        body = "\n".join(f"• {escape(m)}" for m in mistakes)
        console.print(Panel(body, title="[bold yellow]Common Mistakes[/bold yellow]",
                            border_style="yellow", padding=(1, 2)))

    def _hint(self, mission: Mission):
        used = self.progress.hints_used(mission.id)
        if not mission.hints:
            console.print("\n[yellow]This mission has no hints.[/yellow]\n")
        else:
            # Show every hint unlocked so far, plus the next one.
            upto = min(used + 1, len(mission.hints))
            if used < len(mission.hints):
                self.progress.use_hint(mission.id, used)
            body = "\n\n".join(
                f"[bold yellow]💡 Hint {i + 1}/{len(mission.hints)}[/bold yellow]\n{escape(h)}"
                for i, h in enumerate(mission.hints[:upto])
            )
            if used >= len(mission.hints):
                body += "\n\n[dim]No more hints. The solution (S) is the last resort.[/dim]"
            console.print()
            console.print(Panel(body, border_style="yellow", padding=(1, 2)))
            console.print()
        self._pause()

    def _reset(self, mission: Mission):
        console.print()
        confirm = Prompt.ask("[yellow]Throw away your edits and restore the original broken.py?[/yellow]",
                             choices=["y", "n"], default="n")
        if confirm == "y":
            if reset_sandbox(self.sandbox, mission.path):
                console.print("[green]Reset complete.[/green]")
            else:
                console.print("[red]Could not reset - the mission's broken.py is missing.[/red]")
        console.print()
        self._pause()

    def _solution(self, mission: Mission):
        console.print()
        confirm = Prompt.ask("[yellow]⚠  Viewing the solution is recorded in your progress. Continue?[/yellow]",
                             choices=["y", "n"], default="n")
        if confirm == "y":
            self.progress.view_solution(mission.id)
            try:
                code = mission.solution_path.read_text(encoding="utf-8")
                console.print(Panel(Syntax(code, "python", theme="monokai", line_numbers=True),
                                    title="[bold]solution.py[/bold]", border_style="yellow"))
            except OSError as exc:
                console.print(f"[red]Could not read solution: {escape(str(exc))}[/red]")
        console.print()
        self._pause()

    # ------------------------------------------------------------ browser

    def _mission_browser(self, current: Optional[Mission] = None) -> Optional[Mission]:
        """Paged list of all missions. Returns the picked mission or None."""
        page = (self.missions.index(current) // PAGE_SIZE) if current in self.missions else 0
        pages = (len(self.missions) + PAGE_SIZE - 1) // PAGE_SIZE
        by_number = {m.number.lstrip("0") or "0": m for m in self.missions}

        while True:
            self._print_header(compact=True)
            self._print_xp_bar()
            table = Table(box=box.SIMPLE_HEAVY, header_style="bold cyan", expand=True)
            table.add_column("#", style="dim", width=4)
            table.add_column("Mission", ratio=3)
            table.add_column("Level", width=14)
            table.add_column("Category", ratio=2)
            table.add_column("Difficulty", width=10)
            table.add_column("XP", width=4, justify="right")
            table.add_column("", width=3)
            for m in self.missions[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]:
                style = LEVEL_STYLE[m.level]
                marker = "[green]✓[/green]" if self.progress.is_completed(m.id) else ("[cyan]▶[/cyan]" if m is current else "")
                table.add_row(m.number, escape(m.title), f"[{style}]{LEVEL_EMOJI[m.level]} {m.level}[/{style}]",
                              escape(m.category), m.difficulty_stars, str(m.xp), marker)
            console.print(table)
            console.print(f"[dim]Page {page + 1}/{pages}  ·  [b]n[/b] next  [b]p[/b] previous  "
                          f"[b]b[/b]/[b]i[/b]/[b]a[/b] jump to beginner/intermediate/advanced  ·  "
                          f"type a mission number to play  ·  Enter to go back[/dim]")
            choice = Prompt.ask("[dim]Choose[/dim]", default="", show_default=False).strip().lower()
            if choice == "":
                return None
            if choice == "n":
                page = min(pages - 1, page + 1)
            elif choice == "p":
                page = max(0, page - 1)
            elif choice in ("b", "i", "a"):
                level = {"b": "beginner", "i": "intermediate", "a": "advanced"}[choice]
                first = next((i for i, m in enumerate(self.missions) if m.level == level), 0)
                page = first // PAGE_SIZE
            elif choice.isdigit() and (choice.lstrip("0") or "0") in by_number:
                return by_number[choice.lstrip("0") or "0"]

    # ------------------------------------------------------------ progress / endings

    def _show_progress(self):
        self._print_header(compact=True)
        xp = self._xp()
        next_rank, needed = self.progress.next_rank_for(xp)
        next_line = (f"  [dim]{needed:,} XP until {next_rank}[/dim]" if next_rank
                     else "  [bold yellow]Maximum rank reached![/bold yellow]")
        console.print(Panel(
            f"  [cyan]Player:[/cyan]     [bold]{escape(self.progress.player_name())}[/bold]\n"
            f"  [cyan]Rank:[/cyan]       [bold]{self.progress.rank_for(xp)}[/bold]\n"
            f"  [cyan]Total XP:[/cyan]   [bold yellow]{xp:,}[/bold yellow]\n"
            f"  [cyan]Completed:[/cyan]  {self._done()} / {len(self.missions)} missions\n"
            f"  [cyan]Solutions:[/cyan]  {len(self.progress.solutions_viewed())} viewed\n" + next_line,
            title="[bold]YOUR PROGRESS[/bold]", border_style="cyan", padding=(1, 2)))
        console.print()
        for level in LEVELS:
            ms = [m for m in self.missions if m.level == level]
            if not ms:
                continue
            done = sum(1 for m in ms if self.progress.is_completed(m.id))
            width = 40
            filled = int(done / len(ms) * width)
            style = LEVEL_STYLE[level]
            console.print(f"  [{style}]{LEVEL_EMOJI[level]} {level.capitalize():<13}[/{style}]"
                          f"[green]{'█' * filled}[/green][dim]{'░' * (width - filled)}[/dim]  "
                          f"[dim]{done}/{len(ms)}[/dim]")
        console.print()
        self._pause("Press Enter to go back")

    def _campaign_complete(self):
        self._print_header()
        console.print(Panel(
            f"[bold green]Every mission is complete. Outstanding work, {escape(self.progress.player_name())}![/bold green]\n\n"
            "[dim]You can replay any mission from the list.[/dim]",
            border_style="green", padding=(1, 2)))
        self._pause()

    def _goodbye(self):
        console.clear()
        console.print()
        xp = self._xp()
        console.print(Panel(
            f"[bold cyan]Thanks for playing Python Missions, {escape(self.progress.player_name() or 'Operator')}![/bold cyan]\n\n"
            "[dim]Every bug you fixed made you a better engineer. Your edits are saved in sandbox/.[/dim]\n\n"
            f"  Rank:  [bold]{self.progress.rank_for(xp)}[/bold]\n"
            f"  XP:    [bold yellow]{xp:,}[/bold yellow]\n"
            f"  Done:  {self._done()} / {len(self.missions)} missions",
            border_style="cyan", padding=(2, 6)))
        console.print()
