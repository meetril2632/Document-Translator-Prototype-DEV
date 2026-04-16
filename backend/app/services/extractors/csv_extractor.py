"""
Extract text from CSV files.

Preserves delimiter and encoding in meta so the rebuilder can write
the same format back.
"""

import csv
import io
from pathlib import Path

from app.services.extractors.base import ExtractionResult, Segment, SegmentType


def detect_delimiter(sample: str) -> str:
    """Sniff delimiter from first line (comma vs semicolon vs tab)."""
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        return dialect.delimiter
    except Exception:
        return ","


def extract_csv(path: Path, encoding: str = "utf-8") -> ExtractionResult:
    """
    Read CSV and return one segment per row (list of cell strings).
    Empty rows are kept to preserve structure.

    :param path: Path to the CSV file
    :param encoding: File encoding (default utf-8)
    :return: ExtractionResult with segments of type ROW and meta (delimiter, encoding)
    """
    # Read raw bytes and decode; try utf-8 first, then common fallbacks
    raw = path.read_bytes()
    for enc in (encoding, "utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            encoding = enc
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
        encoding = "utf-8"

    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    delimiter = detect_delimiter(text.split("\n")[0]) if text else ","

    segments = []
    for i, row in enumerate(rows):
        segments.append(
            Segment(index=i, content=row, segment_type=SegmentType.ROW, meta={})
        )

    return ExtractionResult(
        segments=segments,
        format="csv",
        meta={"delimiter": delimiter, "encoding": encoding},
    )
