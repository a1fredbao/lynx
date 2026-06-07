from pathlib import Path
from zipfile import ZipFile

from lynx.sdk import Packer, codesnap


def test_packer_add_file_and_build(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "homework").mkdir()
    (tmp_path / "homework" / "report.txt").write_text("hello", encoding="utf-8")

    packer = Packer()
    packer.add_file("homework/report.txt", dest_path="Submission_Report.txt")
    zip_path = packer.build("Final_Submission")

    assert Path(zip_path).exists()
    with ZipFile(zip_path) as archive:
        assert "Submission_Report.txt" in archive.namelist()


def test_packer_add_folder_respects_gitignore_and_patterns(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gitignore").write_text("*.csv\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "keep.py").write_text("print(1)", encoding="utf-8")
    (tmp_path / "src" / "drop.csv").write_text("1,2", encoding="utf-8")
    (tmp_path / "src" / "skip.log").write_text("skip", encoding="utf-8")

    packer = Packer()
    packer.add_folder("src", dest_dir="source", ignore_patterns=["*.log"])
    zip_path = packer.build("final")

    with ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        assert "source/keep.py" in names
        assert "source/drop.csv" not in names
        assert "source/skip.log" not in names


def test_codesnap_creates_png(tmp_path: Path) -> None:
    src = tmp_path / "main.py"
    src.write_text("print('a')\nprint('b')\nprint('c')\n", encoding="utf-8")
    out = tmp_path / "output" / "snap.png"

    result = codesnap(str(src), lines=(1, 2), output_path=str(out))

    assert Path(result).exists()
    assert Path(result).suffix == ".png"
