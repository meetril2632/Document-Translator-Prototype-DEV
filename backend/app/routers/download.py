"""
Download endpoint: return the translated file for a job_id.
Sends the file with the translated filename and optional cleanup after send.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings
from app.utils.filename import download_name_path

router = APIRouter()


@router.get("/download/{job_id}")
def download_translated(job_id: str):
    """
    Download the translated file for this job_id.
    Returns 404 if job or translated file not found.
    """
    # Sanitize: only allow alphanumeric and hyphen (UUID format)
    if not job_id.replace("-", "").isalnum() or len(job_id) > 64:
        raise HTTPException(400, "Invalid job_id")

    temp_dir = settings.temp_dir
    # Translated file is stored as {job_id}_translated{ext}
    candidates = list(temp_dir.glob(f"{job_id}_translated*"))
    if not candidates:
        raise HTTPException(404, "Translated file not found. Run translate first.")

    path = candidates[0]
    if not path.is_file():
        raise HTTPException(404, "Translated file not found.")

    # Translated basename written by pipeline (UTF-8); fallback for older jobs
    name_file = download_name_path(temp_dir, job_id)
    if name_file.is_file():
        filename = name_file.read_text(encoding="utf-8").strip() or path.name
    else:
        meta_path = temp_dir / f"{job_id}_meta.txt"
        if meta_path.exists():
            original = meta_path.read_text(encoding="utf-8").strip()
            stem = Path(original).stem
            ext = Path(original).suffix
            filename = f"{stem}_translated{ext}"
        else:
            filename = path.name

    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=filename,
    )
