"""
Offline translation using Argos Translate.

No content is sent to any external API; models run locally.
Language packs must be installed via Argos (e.g. download from package index).
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Force Argos to avoid Stanza sentence splitter, which may try to fetch
# resources_*.json from raw.githubusercontent.com on first use.
# MiniSBD is more offline-friendly for local-only translation.
# Use direct assignment (not setdefault) so this wins even if inherited env differs.
os.environ["ARGOS_CHUNK_TYPE"] = "MINISBD"

# Cache translation objects per (source, target) to avoid repeated lookups
_translation_cache: dict[tuple[str, str], object] = {}


def _get_translation(source_lang: str, target_lang: str):
    """
    Get Argos translation object for the given language pair.
    Cached per process. Uses argostranslate.translate.get_installed_languages().
    """
    try:
        import argostranslate.settings as argos_settings
        import argostranslate.translate
    except ImportError:
        raise RuntimeError(
            "argostranslate is not installed. Run: pip install argostranslate"
        )

    # Extra safety: force runtime chunk mode in-process, independent of env-file load order.
    try:
        argos_settings.chunk_type = argos_settings.ChunkType.MINISBD
    except Exception:
        # If internals change, keep going; env var above still applies.
        pass

    source_lang = source_lang.lower()
    target_lang = target_lang.lower()
    key = (source_lang, target_lang)
    if key in _translation_cache:
        return _translation_cache[key]

    installed = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed if l.code == source_lang), None)
    to_lang = next((l for l in installed if l.code == target_lang), None)
    if from_lang is None:
        raise ValueError(f"Language '{source_lang}' is not installed. Install the Argos language pack.")
    if to_lang is None:
        raise ValueError(f"Language '{target_lang}' is not installed. Install the Argos language pack.")

    try:
        translation = from_lang.get_translation(to_lang)
        if translation is None:
            raise ValueError(
                f"No translation package installed for {source_lang} -> {target_lang}. "
                "Use the Argos GUI or package index to install the language pair."
            )
        _translation_cache[key] = translation
        return translation
    except Exception as e:
        logger.exception("Failed to get Argos translation %s -> %s", source_lang, target_lang)
        raise ValueError(
            f"Translation not available for {source_lang} -> {target_lang}. "
            "Install the language pair package."
        ) from e


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    translation: Optional[object] = None,
) -> str:
    """
    Translate a single string. Uses cached translation if not provided.

    :param text: Source text
    :param source_lang: Source language code (e.g. en)
    :param target_lang: Target language code (e.g. es)
    :param translation: Optional pre-obtained translation object (avoids lookup)
    :return: Translated text
    """
    if not text or not text.strip():
        return text

    if translation is None:
        translation = _get_translation(source_lang, target_lang)
    try:
        return translation.translate(text)
    except Exception as e:
        # Offline environments sometimes fail when Argos/Stanza attempts to
        # download sentence resources from GitHub (raw.githubusercontent.com).
        # Return a clear actionable error instead of a raw traceback.
        msg = str(e).lower()
        if (
            "raw.githubusercontent.com" in msg
            or "stanza" in msg
            or "httpsconnectionpool" in msg
            or "name resolution" in msg
            or "getaddrinfo failed" in msg
        ):
            raise RuntimeError(
                "Offline translation failed because a sentence-splitting dependency attempted "
                "an internet fetch. The app is configured to use MiniSBD offline mode. "
                "Please restart the backend and try again. If it still happens, reinstall the "
                "Argos language packs while online once, then retry offline."
            ) from e
        raise


def get_installed_pairs() -> list[tuple[str, str]]:
    """
    Return list of (from_code, to_code) for installed Argos translation packages.
    Used by /api/languages to show available pairs.
    """
    try:
        import argostranslate.package
    except ImportError:
        return []

    # IMPORTANT:
    # Do NOT call from_lang.get_translation(to_lang) here.
    # That may instantiate/cached translation objects and lock in an SBD mode
    # (e.g. Stanza) before our runtime override to MINISBD is applied.
    # Instead, read installed package metadata directly.
    pairs: list[tuple[str, str]] = []
    try:
        for pkg in argostranslate.package.get_installed_packages():
            if getattr(pkg, "type", None) == "translate":
                from_code = getattr(pkg, "from_code", None)
                to_code = getattr(pkg, "to_code", None)
                if from_code and to_code and from_code != to_code:
                    pairs.append((from_code, to_code))
    except Exception as e:
        logger.warning("Could not list Argos package pairs: %s", e)
    return sorted(list(set(pairs)))
