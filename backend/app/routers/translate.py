"""
Translate endpoint: run extract -> translate -> rebuild for a job_id.
Returns translated filename for download on success.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.translate import TranslateRequest, TranslateResponse
from app.services.pipeline import run_translation_pipeline

router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
def translate_document(body: TranslateRequest):
    """
    Run offline translation for an uploaded file.
    Requires job_id from upload and source/target language codes from /api/languages.
    """
    translated_filename, error = run_translation_pipeline(
        body.job_id,
        body.source_lang,
        body.target_lang,
    )
    if error:
        raise HTTPException(400, error)
    return TranslateResponse(
        job_id=body.job_id,
        status="ok",
        translated_filename=translated_filename,
    )
