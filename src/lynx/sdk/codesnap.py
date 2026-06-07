from __future__ import annotations

import sys
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
    return ["DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono", "Courier New"]


def _build_formatter(theme: str) -> ImageFormatter:
    last_error: FontNotFound | None = None
    for font_name in _font_candidates():
        try:
            return ImageFormatter(style=theme, line_numbers=True, font_name=font_name)
        except FontNotFound as error:
            last_error = error

    if last_error is not None:
        raise last_error
    raise RuntimeError("No font candidates configured")


def codesnap(src_file: str, lines: tuple[int, int], output_path: str, theme: str = "monokai") -> str:
    src = Path(src_file)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src_file}")

    start, end = lines
    if start < 1 or end < start:
        raise ValueError("lines must be a tuple(start, end) with start >= 1 and end >= start")

    all_lines = src.read_text(encoding="utf-8").splitlines()
    snippet = "\n".join(all_lines[start - 1 : end])
    if not snippet:
        raise ValueError("The requested line range is empty")

    try:
        lexer = get_lexer_for_filename(src.name, snippet)
    except Exception:
        lexer = guess_lexer(snippet)

    formatter = _build_formatter(theme)
    image_data = highlight(snippet, lexer, formatter)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    out.write_bytes(image_data)

    return str(out)
