"""Schemas for languages endpoint."""

from pydantic import BaseModel, Field


class LanguagePair(BaseModel):
    """A supported source -> target language pair."""

    source: str = Field(..., description="Source language code")
    target: str = Field(..., description="Target language code")
    source_name: str | None = Field(default=None, description="Display name for source")
    target_name: str | None = Field(default=None, description="Display name for target")


class LanguagesResponse(BaseModel):
    """List of available language pairs (from installed Argos packs)."""

    pairs: list[LanguagePair] = Field(default_factory=list)
    # Flat list of unique language codes for dropdowns
    languages: list[str] = Field(default_factory=list)
