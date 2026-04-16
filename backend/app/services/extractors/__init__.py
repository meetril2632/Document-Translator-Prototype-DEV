"""
Text extraction from supported file formats.

Each module returns a structured representation (e.g. list of segments or rows)
that can be translated and then passed to the corresponding rebuilder.
"""

from app.services.extractors.base import ExtractionResult, Segment
from app.services.extractors.csv_extractor import extract_csv
from app.services.extractors.docx_extractor import extract_docx
from app.services.extractors.txt_extractor import extract_txt
from app.services.extractors.xlsx_extractor import extract_xlsx

__all__ = [
    "ExtractionResult",
    "Segment",
    "extract_csv",
    "extract_docx",
    "extract_txt",
    "extract_xlsx",
]
