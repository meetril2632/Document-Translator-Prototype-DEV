"""
Languages endpoint: list installed Argos language pairs for the UI dropdowns.
"""

from fastapi import APIRouter

from app.schemas.languages import LanguagePair, LanguagesResponse
from app.services.translation import get_installed_pairs

router = APIRouter()


@router.get("/languages", response_model=LanguagesResponse)
def list_languages():
    """
    Return installed Argos translation pairs and a flat list of language codes.
    If no packs are installed, returns empty lists (install e.g. en-es pack).
    """
    pairs_tuples = get_installed_pairs()
    pairs = [
        LanguagePair(source=p[0], target=p[1], source_name=p[0].upper(), target_name=p[1].upper())
        for p in pairs_tuples
    ]
    languages = sorted(set(p[0] for p in pairs_tuples) | set(p[1] for p in pairs_tuples))
    return LanguagesResponse(pairs=pairs, languages=languages)
