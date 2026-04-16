"""
Base types for extraction results.

Extractors produce a list of segments (or structured data) that we translate
and then pass to rebuilders to write back into the same format.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SegmentType(str, Enum):
    """Type of content segment (for format-specific rebuild)."""
    TEXT = "text"       # Plain string to translate
    ROW = "row"         # CSV row (list of cells)
    PARAGRAPH = "paragraph"  # DOCX paragraph (list of runs)
    CELL = "cell"       # Single cell (e.g. Excel)


@dataclass
class Segment:
    """
    A single translatable segment with optional metadata for rebuild.
    """
    # Unique index for ordering
    index: int
    # Content: string for simple text, or list/dict for structured (e.g. row of cells)
    content: Any
    # Type hint for rebuilder
    segment_type: SegmentType = SegmentType.TEXT
    # Optional: style or position info for format preservation
    meta: dict = field(default_factory=dict)


@dataclass
class ExtractionResult:
    """
    Result of extracting content from a file.
    - segments: ordered list of segments to translate
    - format: file format (csv, docx, xlsx, pdf) for routing to rebuilder
    - meta: format-specific metadata (e.g. CSV delimiter, encoding)
    """
    segments: list[Segment]
    format: str
    meta: dict = field(default_factory=dict)
