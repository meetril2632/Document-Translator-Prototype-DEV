"""Schemas for translate endpoint."""

from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Request body for starting translation."""

    job_id: str = Field(..., description="Job ID from upload")
    source_lang: str = Field(..., description="Source language code (e.g. en)")
    target_lang: str = Field(..., description="Target language code (e.g. es)")


class TranslateResponse(BaseModel):
    """Returned when translation has finished."""

    job_id: str
    status: str = Field(default="ok", description="ok | error")
    message: str | None = Field(default=None, description="Error message if status != ok")
    translated_filename: str | None = Field(
        default=None, description="Filename of translated file for download"
    )
