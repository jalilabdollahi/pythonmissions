"""Main TUI - all screens and game loop."""

import getpass
import time
from pathlib import Path
from typing import List

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from .missions import Mission, load_missions
from .progress import Progress
from .runner import open_editor, reset_mission, run_tests
from .sandbox import prepare_sandbox

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

LEVEL_STYLE = {
    "beginner": "bold green",
    "intermediate": "bold yellow",
    "advanced": "bold red",
}
LEVEL_EMOJI = {
    "beginner": "🟢",
    "intermediate": "🟡",
    "advanced": "🔴",
}
LEVEL_BORDER = {
    "beginner": "green",
    "intermediate": "yellow",
    "advanced": "red",
}


class GameUI:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.missions: List[Mission] = []
        self.progress = Progress()
        self.active_sandbox_path: Path | None = None

    def run(self):
        self.missions = load_missions(self.base_path)
        if not self.missions:
            console.print("[red]No missions found! Check the missions/ directory.[/red]")
            return

        self._ensure_player_name()

        while True:
            mission = self._next_mission()
            if mission is None:
                self._goodbye()
                break
            self.active_sandbox_path = prepare_sandbox(self.base_path, mission.path)
            action = self._play_mission(mission)
            if action == "quit":
                self._goodbye()
                break

    def _ensure_player_name(self):
        if self.progress.player_name():
            return

        self._print_header()
        console.print("[bold]WELCOME, OPERATOR[/bold]\n")
        console.print("This campaign starts from the easiest mission and moves forward one level at a time.\n")

        default_name = getpass.getuser() or "DevOps Agent"
        name = Prompt.ask("[cyan]Your name[/cyan]", default=default_name).strip()
        self.progress.set_player_name(name or default_name)

    def _next_mission(self) -> Mission | None:
        return next((mission for mission in self.missions if not self.progress.is_completed(mission.id)), None)

    def _print_header(self):
        console.clear()
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
        xp = self.progress.total_xp()
        done = self.progress.completed_count()
        total = len(self.missions)
        rank = self.progress.get_rank()
        next_rank, xp_needed = self.progress.next_rank_info()

        filled = int((done / total) * 24) if total else 0
        bar = "[green]" + "█" * filled + "[/green][dim]" + "░" * (24 - filled) + "[/dim]"

        line = f"[cyan]Rank:[/cyan] [bold]{rank}[/bold]  [cyan]XP:[/cyan] [bold yellow]{xp}[/bold yellow]"
        if next_rank:
            line += f"  [dim](+{xp_needed} to {next_rank})[/dim]"
        line += f"  {bar}  [dim]{done}/{total}[/dim]"
        console.print(line)
        player_name = self.progress.player_name()
        if player_name:
            console.print(f"[cyan]Player:[/cyan] [bold]{player_name}[/bold]")
        console.print()

    def _main_menu(self) -> str:
        self._print_header()
        self._print_xp_bar()

        next_m = next((m for m in self.missions if not self.progress.is_completed(m.id)), None)

        console.print("[bold]MAIN MENU[/bold]")
        console.print()
        console.print("  [cyan][1][/cyan]  Browse All Missions")
        if next_m:
            console.print(f"  [cyan][2][/cyan]  Continue  →  [bold]{next_m.title}[/bold]  [dim]({next_m.id})[/dim]")
        else:
            console.print("  [cyan][2][/cyan]  [dim]All missions complete! 🎉[/dim]")
        console.print("  [cyan][3][/cyan]  My Progress")
        console.print("  [cyan][q][/cyan]  Quit")
        console.print()

        choice = Prompt.ask("[dim]Choose[/dim]", choices=["1", "2", "3", "q"], default="1")

        if choice == "1":
            self._mission_browser()
        elif choice == "2" and next_m:
            self._play_mission(next_m)
        elif choice == "3":
            self._show_progress()
        elif choice == "q":
            return "quit"
        return "continue"

    def _mission_browser(self):
        while True:
            self._print_header()
            console.print("[bold]ALL MISSIONS[/bold]\n")

            table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan", pad_edge=True)
            table.add_column("#", style="dim", width=4)
            table.add_column("Mission", min_width=26)
            table.add_column("Level", width=15)
            table.add_column("Category", width=16)
            table.add_column("Difficulty", width=12)
            table.add_column("XP", width=6)
            table.add_column("Status", width=9)

            for i, mission in enumerate(self.missions, 1):
                done = self.progress.is_completed(mission.id)
                style = LEVEL_STYLE[mission.level]
                emoji = LEVEL_EMOJI[mission.level]
                status = "[green]✓ Done[/green]" if done else "[dim]○ Open[/dim]"
                table.add_row(
                    str(i),
                    f"[bold]{mission.title}[/bold]",
                    f"[{style}]{emoji} {mission.level.capitalize()}[/{style}]",
                    mission.category,
                    mission.difficulty_stars,
                    str(mission.xp),
                    status,
                )

            console.print(table)
            console.print()
            console.print("[dim]Enter a number to play, or [b]b[/b] to go back[/dim]")

            choices = [str(i) for i in range(1, len(self.missions) + 1)] + ["b"]
            choice = Prompt.ask("[dim]Choose[/dim]", choices=choices, default="b")

            if choice == "b":
                break
            self._play_mission(self.missions[int(choice) - 1])

    def _play_mission(self, mission: Mission) -> str:
        sandbox_path = self._sandbox_path()

        while True:
            self._print_header()
            emoji = LEVEL_EMOJI[mission.level]
            style = LEVEL_STYLE[mission.level]
            border = LEVEL_BORDER[mission.level]
            done = self.progress.is_completed(mission.id)

            console.print(
                Panel(
                    f"[bold white]{mission.title}[/bold white]\n\n[dim]{mission.story}[/dim]",
                    title=f"[{style}]{emoji} {mission.level.upper()}  ·  {mission.category}  ·  {mission.difficulty_stars}  ·  {mission.xp} XP[/{style}]",
                    border_style=border,
                    padding=(1, 2),
                )
            )

            console.print(
                Panel(
                    mission.description,
                    title="[bold]Mission Brief[/bold]",
                    border_style="blue",
                    padding=(0, 2),
                )
            )
            console.print()
            console.print("[dim]Use [E] Edit to open the mission file in your editor.[/dim]")
            console.print()

            if done:
                console.print("[bold green]  ✓ MISSION COMPLETE![/bold green]\n")

            hints_left = len(mission.hints) - self.progress.hints_used(mission.id)
            has_solution = mission.solution_path.exists()

            menu_items = [
                "[cyan][E][/cyan] Edit",
                "[cyan][T][/cyan] Test",
                f"[cyan][H][/cyan] Hint [dim]({hints_left})[/dim]",
                "[cyan][R][/cyan] Reset",
                "[cyan][P][/cyan] Progress",
            ]
            if has_solution:
                menu_items.append("[cyan][S][/cyan] Solution")
            menu_items.append("[cyan][Q][/cyan] Quit")
            console.print("  " + "  ".join(menu_items))
            console.print()

            valid = ["e", "t", "h", "r", "p", "q"] + (["s"] if has_solution else [])
            choice = Prompt.ask("[dim]Action[/dim]", choices=valid, default="t")

            if choice == "q":
                return "quit"
            if choice == "e":
                self._edit(mission)
            elif choice == "t":
                if self._test(mission):
                    return "advance"
            elif choice == "h":
                self._hint(mission)
            elif choice == "r":
                self._reset(mission)
            elif choice == "p":
                self._show_progress()
            elif choice == "s":
                self._solution(mission)

    def _edit(self, mission: Mission):
        editor = __import__("engine.runner", fromlist=["get_editor"]).get_editor()
        console.print(f"\n[dim]Opening broken.py in {editor}... Save and close when done.[/dim]\n")
        time.sleep(0.8)
        ok, err = open_editor(self._sandbox_path() / "broken.py")
        if not ok:
            console.print(f"[red]Could not open editor: {err}[/red]")
            console.print("[dim]You can also edit the file manually:[/dim]")
            console.print(f"[bold]{self._sandbox_path() / 'broken.py'}[/bold]\n")
            Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def _test(self, mission: Mission) -> bool:
        self.progress.record_attempt(mission.id)
        console.print()
        console.print(Rule("[bold]Running Tests[/bold]"))
        console.print()

        with console.status("[cyan]Running tests...[/cyan]", spinner="dots"):
            passed, output, failed = run_tests(self._sandbox_path())

        if passed:
            console.print(
                Panel(
                    "[bold green]✓ ALL TESTS PASSED![/bold green]\n\n[dim]" + output + "[/dim]",
                    border_style="green",
                    padding=(1, 2),
                )
            )
            if not self.progress.is_completed(mission.id):
                self.progress.complete_mission(mission.id, mission.xp)
                rank = self.progress.get_rank()
                console.print(f"\n[bold yellow]🎉 +{mission.xp} XP earned![/bold yellow]")
                console.print(f"[bold]Current rank: {rank}[/bold]\n")
                next_rank, needed = self.progress.next_rank_info()
                if next_rank:
                    console.print(f"[dim]{needed} XP until {next_rank}[/dim]\n")
            self._show_post_level_lesson(mission)
            next_mission = self._next_mission()
            if next_mission is not None:
                console.print(f"[bold cyan]Next mission:[/bold cyan] {next_mission.title}")
            else:
                console.print("[bold cyan]Campaign complete![/bold cyan]")
            self._wait_for_next_level()
            return True
        else:
            lines = []
            for line in output.splitlines():
                if "PASSED" in line:
                    lines.append(f"[green]  ✓ {line.strip()}[/green]")
                elif "FAILED" in line or "ERROR" in line:
                    lines.append(f"[red]  ✗ {line.strip()}[/red]")
                elif line.strip():
                    lines.append(f"[dim]  {line}[/dim]")
            body = "[bold red]✗ TESTS FAILED[/bold red]\n\n" + "\n".join(lines)
            console.print(Panel(body, border_style="red", padding=(1, 2)))

            hints_left = len(mission.hints) - self.progress.hints_used(mission.id)
            if hints_left > 0:
                console.print(f"\n[dim]Tip: press [H] to get a hint ({hints_left} remaining)[/dim]")

        console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
        return False

    def _hint(self, mission: Mission):
        used = self.progress.hints_used(mission.id)
        if used >= len(mission.hints):
            console.print("\n[yellow]No more hints for this mission.[/yellow]\n")
        else:
            hint_text = mission.hints[used]
            self.progress.use_hint(mission.id, used)
            console.print()
            console.print(
                Panel(
                    f"[bold yellow]💡 Hint {used + 1} of {len(mission.hints)}[/bold yellow]\n\n{hint_text}",
                    border_style="yellow",
                    padding=(1, 2),
                )
            )
            console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def _reset(self, mission: Mission):
        console.print()
        confirm = Prompt.ask(
            "[yellow]Reset broken.py to the original broken version?[/yellow]",
            choices=["y", "n"],
            default="n",
        )
        if confirm == "y":
            if reset_mission(self._sandbox_path()):
                console.print("[green]Reset complete.[/green]")
            else:
                console.print("[red]Could not reset - original.py not found.[/red]")
        console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def _solution(self, mission: Mission):
        console.print()
        confirm = Prompt.ask(
            "[yellow]⚠  Viewing the solution will be recorded. Continue?[/yellow]",
            choices=["y", "n"],
            default="n",
        )
        if confirm == "y":
            self.progress.view_solution(mission.id)
            try:
                code = mission.solution_path.read_text(encoding="utf-8")
                syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title="[bold]solution.py[/bold]", border_style="yellow"))
            except Exception as e:
                console.print(f"[red]Could not read solution: {e}[/red]")
        console.print()
        Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

    def _show_progress(self):
        self._print_header()
        xp = self.progress.total_xp()
        done = self.progress.completed_count()
        rank = self.progress.get_rank()
        solutions = len(self.progress.solutions_viewed())
        total = len(self.missions)

        next_rank, needed = self.progress.next_rank_info()
        next_line = f"  [dim]{needed} XP until {next_rank}[/dim]" if next_rank else "  [bold yellow]Maximum rank reached![/bold yellow]"

        console.print(
            Panel(
                f"  [cyan]Rank:[/cyan]       [bold]{rank}[/bold]\n"
                f"  [cyan]Total XP:[/cyan]   [bold yellow]{xp}[/bold yellow]\n"
                f"  [cyan]Completed:[/cyan]  {done} / {total} missions\n"
                f"  [cyan]Solutions:[/cyan]  {solutions} viewed\n"
                + next_line,
                title="[bold]YOUR PROGRESS[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )
        console.print()

        for level in ["beginner", "intermediate", "advanced"]:
            missions = [m for m in self.missions if m.level == level]
            done_ms = [m for m in missions if self.progress.is_completed(m.id)]
            style = LEVEL_STYLE[level]
            emoji = LEVEL_EMOJI[level]
            bar = "[green]" + "█" * len(done_ms) + "[/green][dim]" + "░" * (len(missions) - len(done_ms)) + "[/dim]"
            console.print(f"  [{style}]{emoji} {level.capitalize()}[/{style}]  {bar}  [dim]{len(done_ms)}/{len(missions)}[/dim]")

        console.print()
        Prompt.ask("[dim]Press Enter to go back[/dim]", default="")

    def _goodbye(self):
        console.clear()
        console.print()
        console.print(
            Panel(
                f"[bold cyan]Thanks for playing Python Missions, {self.progress.player_name() or 'Operator'}![/bold cyan]\n\n"
                f"[dim]Every bug you fixed made you a better engineer.[/dim]\n\n"
                f"  Rank:  [bold]{self.progress.get_rank()}[/bold]\n"
                f"  XP:    [bold yellow]{self.progress.total_xp()}[/bold yellow]\n"
                f"  Done:  {self.progress.completed_count()} / {len(self.missions)} missions",
                border_style="cyan",
                padding=(2, 6),
            )
        )
        console.print()

    def _sandbox_path(self) -> Path:
        if self.active_sandbox_path is None:
            raise RuntimeError("Sandbox is not prepared for the active mission.")
        return self.active_sandbox_path

    def _show_post_level_lesson(self, mission: Mission):
        debrief = self._build_debrief_text(mission)
        mistakes = self._build_common_mistakes_text(mission)

        console.print()
        console.print(
            Panel(
                Text.assemble(
                    ("Level Complete - lesson unlocked", "bold green"),
                    ("  (debrief + common mistakes)", "bright_yellow"),
                ),
                border_style="green",
                box=box.ROUNDED,
                padding=(0, 1),
            )
        )
        console.print(Panel(debrief, title="[bold green]Debrief[/bold green]", border_style="green", padding=(1, 2)))
        console.print(Panel(mistakes, title="[bold yellow]Common Mistakes[/bold yellow]", border_style="yellow", padding=(1, 2)))

    def _build_debrief_text(self, mission: Mission) -> str:
        concept_line = ", ".join(mission.tags[:4]) if mission.tags else mission.category
        return (
            f"You fixed [bold]{mission.title}[/bold] by correcting the Python issue the mission was teaching.\n\n"
            f"This level focused on [cyan]{mission.category}[/cyan] and practiced: {concept_line}.\n\n"
            "The habit that matters is the same one you will use in real work: reproduce the failure, read the error carefully, "
            "make the smallest correct code change, and prove it with tests."
        )

    def _build_common_mistakes_text(self, mission: Mission) -> str:
        hints = mission.hints or []
        mistake_lines = [
            "1. Fixing symptoms without reading the failing test or traceback first.",
            "2. Making extra refactors instead of the smallest change that gets the mission green.",
        ]
        if hints:
            mistake_lines.append(f"3. Ignoring the mission clues. A strong hint from this level was: {hints[0]}")
        else:
            mistake_lines.append("3. Skipping validation after editing the sandbox copy.")
        return "\n".join(mistake_lines)

    def _wait_for_next_level(self):
        console.print()
        console.print("[dim]Press Enter or Space for the next level[/dim]")
        console.input()
