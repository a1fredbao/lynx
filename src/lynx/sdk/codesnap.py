from __future__ import annotations

import sys
from typing import cast
from pathlib import Path
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.formatters.img import FontNotFound
from pygments.lexers import get_lexer_for_filename, guess_lexer


def _font_candidates() -> list[str]:
    if sys.platform == "darwin":
        return ["Menlo", "SF Mono", "Monaco", "DejaVu Sans Mono", "Courier New"]
    if sys.platform.startswith("win"):
        return ["Consolas", "Cascadia Mono", "Courier New", "DejaVu Sans Mono"]
    if sys.platform.startswith(("linux", "freebsd", "openbsd", "netbsd")):
        return ["DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono", "Courier New"]
    return []


def _build_formatter(theme: str, font_name: str | None = None) -> ImageFormatter:
    candidates = _font_candidates()
    if font_name:
        candidates.insert(0, font_name)

    if not candidates:
        raise FontNotFound("No usable fonts configured for this platform")

    last_error: FontNotFound | None = None
    for font_name in candidates:
        try:
            return ImageFormatter(style=theme, line_numbers=True, font_name=font_name)
        except FontNotFound as error:
            last_error = error

    raise cast(FontNotFound, last_error)


def codesnap(
    src_file: str,
    lines: tuple[int, int] | list[tuple[int, int]],
    output_path: str,
    theme: str = "monokai",
    font_name: str | None = None,
) -> str:
    """
    Generate a syntax-highlighted image snapshot of specific lines from a source code file.

    args:
    - src_file: Path to the source code file.
    - lines: A tuple (start, end) or a list of such tuples specifying line ranges to include in the snapshot. Line numbers are 1-based.
    - output_path: Path where the generated image will be saved.
    - theme: Pygments style to use for syntax highlighting (default: "monokai"). You can choose from any style supported by Pygments
    - font_name: Optional specific font to use.
    """
    src = Path(src_file)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src_file}")

    if isinstance(lines, tuple):
        lines = [lines]

    for start, end in lines:
        if start < 1 or end < start:
            raise ValueError(
                "Every element in lines must be a tuple(start, end) with start >= 1 and end >= start."
            )

    all_lines = src.read_text(encoding="utf-8").splitlines()
    snippet = ""

    for start, end in lines:
        snippet += "\n".join(all_lines[start - 1 : end])

    if not snippet:
        raise ValueError("The requested line range is empty.")

    try:
        lexer = get_lexer_for_filename(src.name, snippet)
    except Exception:
        lexer = guess_lexer(snippet)

    formatter = _build_formatter(theme, font_name)
    image_data = highlight(snippet, lexer, formatter)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    out.write_bytes(image_data)

    return str(out)
