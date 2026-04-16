"""
Orchestrates extract -> translate -> rebuild for a single file.

Uses job_id to resolve file path, detects format from extension,
calls the appropriate extractor, translates all segments via Argos,
then rebuilds to a new file. All processing is synchronous and in-process.
"""

import logging
from pathlib import Path

from app.config import settings
from app.services.extractors import extract_csv, extract_docx, extract_txt, extract_xlsx
from app.services.extractors.base import ExtractionResult, SegmentType
from app.services.rebuild import rebuild
from app.services.translation import translate_text, _get_translation
from app.utils.filename import download_name_path, sanitize_translated_stem

logger = logging.getLogger(__name__)


def get_format_from_extension(filename: str) -> str:
    """Map file extension to our format key (csv, docx, etc.)."""
    ext = Path(filename).suffix.lower()
    if ext == ".csv":
        return "csv"
    if ext in (".docx",):
        return "docx"
    if ext in (".xlsx", ".xls"):
        return "xlsx"
    if ext == ".txt":
        return "txt"
    raise ValueError(f"Unsupported file extension: {ext}")


def extract_file(path: Path, file_format: str) -> ExtractionResult:
    """Dispatch to the right extractor by format."""
    if file_format == "csv":
        return extract_csv(path)
    if file_format == "docx":
        return extract_docx(path)
    if file_format == "xlsx":
        return extract_xlsx(path)
    if file_format == "txt":
        return extract_txt(path)
    raise ValueError(f"No extractor for format: {file_format}")


def run_translation_pipeline(
    job_id: str,
    source_lang: str,
    target_lang: str,
) -> tuple[str, str]:
    """
    Load uploaded file by job_id, extract, translate, rebuild.
    Returns (translated_filename, error_message).
    If error_message is not None, translation failed.
    """
    temp_dir = settings.temp_dir
    # Source file is stored as {job_id}_source{ext} by upload endpoint
    candidates = [f for f in temp_dir.glob(f"{job_id}_source*") if "_translated" not in f.name]
    if not candidates:
        return "", f"Job not found: {job_id}. Upload the file again."
    source_path = candidates[0]

    # Original filename for format detection and download name (stored by upload)
    meta_path = temp_dir / f"{job_id}_meta.txt"
    if meta_path.exists():
        original_filename = meta_path.read_text(encoding="utf-8").strip() or f"document{source_path.suffix}"
    else:
        original_filename = f"document{source_path.suffix}"

    try:
        file_format = get_format_from_extension(original_filename)
    except ValueError as e:
        return "", str(e)

    try:
        extracted = extract_file(source_path, file_format)
    except Exception as e:
        logger.exception("Extraction failed for %s", job_id)
        return "", f"Extraction failed: {e}"

    # Get one translation object for all segments (cache)
    try:
        translation = _get_translation(source_lang, target_lang)
    except ValueError as e:
        return "", str(e)

    # Translate the original file stem for the download filename (same language pair)
    stem = Path(original_filename).stem or "document"
    ext = Path(original_filename).suffix
    try:
        raw_translated_stem = translate_text(stem, source_lang, target_lang, translation)
        translated_stem = sanitize_translated_stem(raw_translated_stem)
    except Exception as e:
        logger.warning("Could not translate filename stem, using fallback: %s", e)
        translated_stem = sanitize_translated_stem(f"{stem}_translated")

    out_filename = f"{translated_stem}{ext}"

    translated_contents = []
    try:
        for seg in extracted.segments:
            if seg.segment_type == SegmentType.ROW:
                # CSV: translate each cell in the row
                translated_row = [
                    translate_text(cell, source_lang, target_lang, translation)
                    for cell in seg.content
                ]
                translated_contents.append(translated_row)
            else:
                # Plain text (e.g. docx run)
                translated_contents.append(
                    translate_text(seg.content, source_lang, target_lang, translation)
                )
    except Exception as e:
        logger.exception("Translation failed for %s", job_id)
        return "", f"Translation failed: {e}"

    output_path = temp_dir / f"{job_id}_translated{ext}"

    try:
        rebuild(source_path, output_path, file_format, translated_contents, extracted.meta)
    except Exception as e:
        logger.exception("Rebuild failed for %s", job_id)
        return "", f"Rebuild failed: {e}"

    # After successful rebuild: persist download basename for Content-Disposition (UTF-8)
    try:
        download_name_path(temp_dir, job_id).write_text(out_filename, encoding="utf-8")
    except OSError as e:
        logger.warning("Could not write download name file: %s", e)

    return out_filename, None
