"""
Rebuild CSV from translated row contents.

Preserves delimiter and encoding from extraction meta.
"""

import csv
from pathlib import Path


def rebuild_csv(
    output_path: Path,
    translated_contents: list[list[str]],
    meta: dict,
) -> None:
    """
    Write translated rows to a new CSV file.

    :param output_path: Path for the output CSV
    :param translated_contents: List of rows, each row is list of translated cell strings
    :param meta: Must contain "delimiter" and "encoding" from extractor
    """
    delimiter = meta.get("delimiter", ",")
    encoding = meta.get("encoding", "utf-8")

    with open(output_path, "w", newline="", encoding=encoding) as f:
        writer = csv.writer(f, delimiter=delimiter)
        for row in translated_contents:
            writer.writerow(row)
