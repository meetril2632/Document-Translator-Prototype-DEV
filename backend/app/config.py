"""
Application configuration loaded from environment variables.

Uses pydantic-settings for validation and .env support.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings. Override via env vars or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # -------------------------------------------------------------------------
    # File upload
    # -------------------------------------------------------------------------
    # Maximum upload size in bytes (default 10 MB)
    max_file_size: int = 10 * 1024 * 1024
    # Directory for temporary uploads and translated files (created if missing)
    temp_dir: Path = Path("temp_uploads")
    # Allowed file extensions (lowercase, with dot)
    # Upload/translate formats supported in this project version.
    allowed_extensions: List[str] = [".xlsx", ".csv", ".docx", ".txt"]

    # -------------------------------------------------------------------------
    # CORS (frontend origin)
    # -------------------------------------------------------------------------
    # Comma-separated origins, e.g. "http://localhost:5173,http://127.0.0.1:5173"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # -------------------------------------------------------------------------
    # Optional: cleanup translated files after this many seconds (0 = no auto)
    # -------------------------------------------------------------------------
    temp_file_ttl_seconds: int = 3600

    def get_cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list for FastAPI."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


# Singleton used across the app
settings = Settings()
