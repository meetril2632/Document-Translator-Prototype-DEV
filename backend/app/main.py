"""
FastAPI application entry point.

Mounts API routes and configures CORS. All translation and file processing
runs on this server; no content is sent to external translation APIs.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import download, languages, translate, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure temp directory exists on startup; optional cleanup on shutdown."""
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    yield
    # Optional: clear very old files on shutdown (could be done in a background task instead)


app = FastAPI(
    title="Translation API",
    description="Upload documents, translate offline with Argos, download with format preserved.",
    version="0.1.0",
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# CORS: allow frontend (React dev server) to call this API
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# API routes (grouped by resource)
# -----------------------------------------------------------------------------
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(languages.router, prefix="/api", tags=["languages"])
app.include_router(translate.router, prefix="/api", tags=["translate"])
app.include_router(download.router, prefix="/api", tags=["download"])


@app.get("/api/health")
def api_health():
    """
    Lightweight health check for the frontend / load balancers.
    If this fails from the browser, the FastAPI server is not running or not reachable.
    """
    return {"ok": True, "service": "translation-api"}


@app.get("/")
def root():
    """Health check / API info."""
    return {
        "service": "translation-api",
        "docs": "/docs",
        "allowed_extensions": settings.allowed_extensions,
        "max_file_size_mb": settings.max_file_size // (1024 * 1024),
    }
