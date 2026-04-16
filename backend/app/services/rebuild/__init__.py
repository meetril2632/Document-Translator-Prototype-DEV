"""
Rebuild translated content back into the original file format.

Each rebuilder takes the extraction result, the list of translated contents
(in same order as segments), and writes a new file.
"""

from app.services.rebuild.csv_rebuild import rebuild_csv
from app.services.rebuild.docx_rebuild import rebuild_docx
from app.services.rebuild.txt_rebuild import rebuild_txt
from app.services.rebuild.xlsx_rebuild import rebuild_xlsx

__all__ = ["rebuild_csv", "rebuild_docx", "rebuild_txt", "rebuild_xlsx"]


def rebuild(
    source_path,
    output_path,
    format: str,
    translated_contents: list,
    meta: dict,
):
    """
    Route to the correct rebuilder by format.
    :param source_path: Original file path (for formats that need to read structure again)
    :param output_path: Where to write the translated file
    :param format: csv | docx | ...
    :param translated_contents: List of translated values in segment order
    :param meta: Format-specific metadata from extraction
    """
    if format == "csv":
        rebuild_csv(output_path, translated_contents, meta)
    elif format == "docx":
        rebuild_docx(source_path, output_path, translated_contents, meta)
    elif format == "txt":
        rebuild_txt(output_path, translated_contents, meta)
    elif format == "xlsx":
        rebuild_xlsx(source_path, output_path, translated_contents, meta)
    else:
        raise ValueError(f"Unsupported rebuild format: {format}")
