from pathlib import Path
from typer.testing import CliRunner
from lynx.cli import app

runner = CliRunner()


def test_course_creates_directory_and_readme(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["course", "Math101"])
    assert result.exit_code == 0
    assert Path("Math101").is_dir()
    assert Path("Math101/README.md").read_text(encoding="utf-8") == "# Math101"


def test_lecture_creates_standard_workspace(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["lecture", "L1"])
    assert result.exit_code == 0
    assert Path("L1/docs/slides").is_dir()
    assert Path("L1/docs/notes").is_dir()
    assert Path("L1/src").is_dir()
    assert Path("L1/output").is_dir()
    assert Path("L1/homework").is_dir()
    assert Path("L1/.gitignore").is_file()
    assert Path("L1/pack.py").is_file()


def test_clean(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    Path("output").mkdir()
    Path("output/final.zip").write_text("zip", encoding="utf-8")
    Path("output/temp.txt").write_text("tmp", encoding="utf-8")
    Path("output/sub").mkdir()
    Path("output/sub/a.txt").write_text("a", encoding="utf-8")
    Path("pkg/__pycache__").mkdir(parents=True)
    Path("pkg/__pycache__/mod.cpython-311.pyc").write_bytes(b"x")
    Path("pkg/x.pyc").write_bytes(b"x")

    result = runner.invoke(app, ["clean"])
    assert result.exit_code == 0
    assert not Path("output/final.zip").exists()
    assert not Path("output/temp.txt").exists()
    assert not Path("output/sub").exists()
    assert not Path("pkg/__pycache__").exists()
    assert not Path("pkg/x.pyc").exists()


def test_pack_errors_when_pack_py_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["pack"])
    assert result.exit_code == 1
    assert "pack.py not found" in result.output
