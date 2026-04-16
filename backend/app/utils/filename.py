"""
Safe download / display filenames after translation.

Keeps Unicode letters (e.g. Chinese, Japanese) where possible; strips characters
that break Windows paths and trims length.
"""

import re
from pathlib import Path


# Characters invalid in Windows file names (also problematic on macOS/Linux in ZIPs)
_INVALID_WIN_CHARS = re.compile(r'[/\\:*?"<>|]')


def sanitize_translated_stem(stem: str, max_len: int = 180) -> str:
    """
    Clean a translated file stem (no extension) for use as a download filename.

    :param stem: Filename without extension, possibly in target language (Unicode OK)
    :param max_len: Max stem length (extension added separately)
    """
    if not stem:
        return "document"
    s = stem.strip()
    s = _INVALID_WIN_CHARS.sub("", s)
    # No trailing dots/spaces (Windows)
    s = s.rstrip(" .")
    if not s:
        return "document"
    return s[:max_len]


def download_name_path(temp_dir: Path, job_id: str) -> Path:
    """Sidecar file written by pipeline with UTF-8 final download basename."""
    return temp_dir / f"{job_id}_download.txt"
