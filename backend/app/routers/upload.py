"""
Upload endpoint: accept a file, store under temp dir with a job_id, return job_id and filename.

Files are stored as {job_id}_source{ext}. Original filename is saved in {job_id}_meta.txt
so the pipeline and download can use it.
"""

import re
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.schemas.upload import UploadResponse

router = APIRouter()


def sanitize_filename(name: str) -> str:
    """Remove path components and unsafe characters; limit length."""
    # Remove any path
    name = Path(name).name
    # Only allow alphanumeric, dash, underscore, dot
    name = re.sub(r"[^\w\s\-.]", "", name)
    name = name.strip() or "document"
    return name[:200]


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a document for translation. Returns job_id to use in translate and download.

    Accepted types: PDF, DOCX, XLSX, CSV (configurable). Max size from config.
    """
    # Validate extension
    ext = Path(file.filename or "").suffix.lower()
    if ext not in settings.allowed_extensions:
        raise HTTPException(
            400,
            f"File type not allowed. Accepted: {', '.join(settings.allowed_extensions)}",
        )

    # Read and size check
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(
            413,
            f"File too large. Max size: {settings.max_file_size // (1024*1024)} MB",
        )

    job_id = str(uuid.uuid4())
    safe_name = sanitize_filename(file.filename or "document")
    source_path = settings.temp_dir / f"{job_id}_source{ext}"
    meta_path = settings.temp_dir / f"{job_id}_meta.txt"

    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    source_path.write_bytes(content)
    meta_path.write_text(safe_name, encoding="utf-8")

    return UploadResponse(job_id=job_id, filename=safe_name)
