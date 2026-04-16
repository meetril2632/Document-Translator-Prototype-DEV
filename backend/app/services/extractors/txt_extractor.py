"""
Extract translatable text from plain .txt files.

For v1 we translate the whole file as one segment so line breaks are preserved
as-is by the translation engine output.
"""

from __future__ import annotations

from pathlib import Path

from app.services.extractors.base import ExtractionResult, Segment, SegmentType


def _read_text_bytes(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def extract_txt(path: Path) -> ExtractionResult:
    text, encoding = _read_text_bytes(path)
    return ExtractionResult(
        segments=[
            Segment(
                index=0,
                content=text,
                segment_type=SegmentType.TEXT,
                meta={},
            )
        ],
        format="txt",
        meta={"encoding": encoding},
    )

