"""Schemas for upload endpoint."""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Returned after a successful file upload."""

    job_id: str = Field(..., description="Unique ID for this translation job")
    filename: str = Field(..., description="Original filename (sanitized)")
