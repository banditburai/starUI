"""CLI command for sorting Tailwind classes in Python files."""

from pathlib import Path

import typer

from ..sort import sort_files
from .utils import console, error, info, status_context, success

_SKIP = {".venv", "venv", "__pycache__", "node_modules", ".git"}


def sort_command(
    paths: list[str] | None = typer.Argument(None, help="Files or directories to sort (default: current directory)"),
    check: bool = typer.Option(False, "--check", help="Check only — exit 1 if changes needed"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """Sort Tailwind classes in Python source files."""
    targets = [Path(p) for p in paths] if paths else [Path.cwd()]

    files: list[Path] = []
    for target in targets:
        if target.is_file() and target.suffix == ".py":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(p for p in target.rglob("*.py") if not (_SKIP & set(p.relative_to(target).parts))))

    if not files:
        error("No .py files found")
        raise typer.Exit(1)

    if verbose:
        info(f"Processing {len(files)} file(s)")

    with status_context("[bold green]Sorting Tailwind classes..."):
        results = sort_files(files, check=check)

    changed = [p for p, c in results.items() if c]

    if changed:
        verb = "would sort" if check else "sorted"
        for p in changed:
            console.print(f"  {verb} [cyan]{p}[/cyan]")

        if check:
            error(f"{len(changed)} file(s) need sorting")
            raise typer.Exit(1)
        else:
            success(f"Sorted {len(changed)} file(s)")
    else:
        success("All files already sorted")
