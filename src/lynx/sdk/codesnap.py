from __future__ import annotations

import io
from pathlib import Path
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_for_filename, guess_lexer


def codesnap(src_file: str, lines: tuple[int, int], output_path: str, theme: str = "monokai") -> str:
    src = Path(src_file)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src_file}")

    start, end = lines
    if start <= 0 or end < start:
        raise ValueError("lines must be a tuple(start, end) with start >= 1 and end >= start")

    all_lines = src.read_text(encoding="utf-8").splitlines()
    snippet = "\n".join(all_lines[start - 1 : end])
    if not snippet:
        raise ValueError("The requested line range is empty")

    try:
        lexer = get_lexer_for_filename(src.name, snippet)
    except Exception:
        lexer = guess_lexer(snippet)

    formatter = ImageFormatter(style=theme, line_numbers=True, font_name="DejaVu Sans Mono")
    image_data = highlight(snippet, lexer, formatter)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    stream = io.BytesIO(image_data)
    out.write_bytes(stream.getvalue())

    return str(out)
