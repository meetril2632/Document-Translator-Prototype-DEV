"""
Rebuild translated .txt file.

For v1 we translated the whole file as one segment, so we simply write the
translated string back as-is.
"""

from __future__ import annotations

from pathlib import Path


def rebuild_txt(output_path: Path, translated_contents: list[str], meta: dict) -> None:
    encoding = meta.get("encoding", "utf-8")
    text = translated_contents[0] if translated_contents else ""
    output_path.write_text(text, encoding=encoding)

