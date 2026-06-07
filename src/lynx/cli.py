import importlib.util
import shutil
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Lynx: Lectures' Yet aNother eXporter")
console = Console()

DEFAULT_GITIGNORE = """# Python cache
__pycache__/
*.py[cod]

# Regeneratable outputs
output/*
"""

PACK_TEMPLATE = """from lynx.sdk import Packer, codesnap

def make_submission():
    packer = Packer()

    # Example: Move and rename a report
    # packer.add_file("homework/report.docx", dest_path="Submission_Report.docx")

    # Example: Pack source code but ignore cache and datasets
    # packer.add_folder("src/", dest_dir="source_code/", ignore_patterns=["*.csv", "__pycache__"])

    # Example: Generate code snapshot and add to pack, putting line (3, 5) after (10, 25) as the sequence in the list.
    # snap_path = codesnap("src/main.py", lines=[(10, 25), (3, 5)], output_path="output/core_logic.png")
    # packer.add_file(snap_path, dest_path="img/core_logic.png")

    packer.build(output_filename="Final_Submission")

if __name__ == "__main__":
    make_submission()
"""


@app.command()
def course(course_name: str) -> None:
    target = Path.cwd() / course_name
    if target.exists():
        console.print(f"[red]Directory already exists:[/red] {target}")
        raise typer.Exit(code=1)

    target.mkdir()
    (target / "README.md").write_text(f"# {course_name}", encoding="utf-8")
    console.print(f"[green]Created course:[/green] {target}")


@app.command()
def lecture(lecture_name: str) -> None:
    root = Path.cwd() / lecture_name
    if root.exists():
        console.print(f"[red]Directory already exists:[/red] {root}")
        raise typer.Exit(code=1)

    for folder in [
        root / "docs" / "slides",
        root / "docs" / "notes",
        root / "src",
        root / "output",
        root / "homework",
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    (root / ".gitignore").write_text(DEFAULT_GITIGNORE, encoding="utf-8")
    (root / "pack.py").write_text(PACK_TEMPLATE, encoding="utf-8")
    console.print(f"[green]Created lecture workspace:[/green] {root}")


@app.command()
def clean() -> None:
    root = Path.cwd()

    for pycache in root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)

    for pyc in root.rglob("*.pyc"):
        if pyc.is_file():
            pyc.unlink(missing_ok=True)

    output_dir = root / "output"
    if output_dir.exists() and output_dir.is_dir():
        for item in output_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)

    console.print("[green]Workspace cleaned.[/green]")


@app.command()
def pack() -> None:
    pack_file = Path.cwd() / "pack.py"
    if not pack_file.exists():
        console.print("[red]pack.py not found in the current directory.[/red]")
        raise typer.Exit(code=1)

    spec = importlib.util.spec_from_file_location("lynx_pack_script", pack_file)
    if spec is None or spec.loader is None:
        console.print("[red]Unable to load pack.py.[/red]")
        raise typer.Exit(code=1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    make_submission = getattr(module, "make_submission", None)
    if make_submission is None or not callable(make_submission):
        console.print("[red]make_submission() is missing in pack.py.[/red]")
        raise typer.Exit(code=1)

    make_submission()
    console.print("[green]Submission package created successfully.[/green]")


if __name__ == "__main__":
    app()
