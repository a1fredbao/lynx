from __future__ import annotations

import fnmatch
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pathspec


class Packer:
    def __init__(self) -> None:
        self.base_dir = Path.cwd()
        self.items: list[tuple[Path, Path]] = []
        self._gitignore_spec = self._load_gitignore_spec()

    def _load_gitignore_spec(self) -> pathspec.PathSpec | None:
        gitignore_file = self.base_dir / ".gitignore"
        if not gitignore_file.exists():
            return None
        lines = gitignore_file.read_text(encoding="utf-8").splitlines()
        return pathspec.PathSpec.from_lines("gitignore", lines)

    def add_file(self, src_path: str, dest_path: str | None = None) -> None:
        """
        Add a single file to the pack.

        If dest_path is not provided, the file will be stored with its path relative to the base directory.

        args:
        - src_path: The path to the source file to be added.
        - dest_path: Optional path to store the file in the archive. If not provided, the file's path relative to the base directory will be used.
        """

        src = (self.base_dir / src_path).resolve()
        if not src.exists() or not src.is_file():
            raise FileNotFoundError(f"File not found: {src_path}")
        if dest_path:
            arcname = Path(dest_path)
        else:
            arcname = src.relative_to(self.base_dir)
        self.items.append((src, arcname))

    def _is_ignored(self, candidate: Path, ignore_patterns: list[str] | None) -> bool:
        relative = candidate.relative_to(self.base_dir).as_posix()

        if self._gitignore_spec and self._gitignore_spec.match_file(relative):
            return True

        if ignore_patterns:
            for pattern in ignore_patterns:
                if fnmatch.fnmatch(candidate.name, pattern) or fnmatch.fnmatch(
                    relative, pattern
                ):
                    return True

        return False

    def add_folder(
        self,
        src_dir: str,
        dest_dir: str | None = None,
        ignore_patterns: list[str] | None = None,
    ) -> None:
        """
        Add a folder and its contents to the pack. The directory structure will be preserved.

        args:
        - src_dir: The path to the source directory to be added.
        - dest_dir: Optional path to store the directory in the archive. If not provided, the directory's path relative to the base directory will be used.
        - ignore_patterns: Optional list of glob patterns to ignore. Patterns will be matched against both the file/directory name and the path relative to the base directory. For example, ["*.csv", "__pycache__"] will ignore all CSV files and any file or directory under a __pycache__ directory.
        """
        source = (self.base_dir / src_dir).resolve()
        if not source.exists() or not source.is_dir():
            raise NotADirectoryError(f"Directory not found: {src_dir}")

        for path in source.rglob("*"):
            if path.is_dir() or self._is_ignored(path, ignore_patterns):
                continue

            rel = path.relative_to(source)
            if dest_dir:
                arcname = Path(dest_dir) / rel
            else:
                arcname = Path(src_dir) / rel
            self.items.append((path, arcname))

    def build(self, output_filename: str) -> str:
        """
        Build the archive with the added files and folders.

        args:
        - output_filename: The name of the output archive file (without extension `.zip`).
        """
        output_dir = self.base_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_zip = output_dir / f"{output_filename}.zip"

        with ZipFile(output_zip, mode="w", compression=ZIP_DEFLATED) as archive:
            for src, dest in self.items:
                archive.write(src, arcname=dest.as_posix())

        return str(output_zip)
