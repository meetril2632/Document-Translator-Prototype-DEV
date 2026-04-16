#!/usr/bin/env python3
"""
Install Argos Translate offline language packs for English, Chinese, Japanese, and German.

Run from the backend folder with the same Python/venv you use for the API:

    cd backend
    .\\venv\\Scripts\\activate          # Windows
    python scripts/install_language_packs.py

This downloads and installs every package in the Argos index where both the source
and target language are in: en, zh, ja, de (so you can translate between these four).

Note: Argos may not offer every pair (e.g. zh->ja). The script installs only pairs
that exist in the official package index.
"""

from __future__ import annotations

import sys

# ISO 639-1 codes used by Argos for these languages
TARGET_LANGS = frozenset({"en", "zh", "ja", "de"})


def main() -> int:
    try:
        import argostranslate.package
    except ImportError:
        print("ERROR: argostranslate is not installed. Run: pip install argostranslate", file=sys.stderr)
        return 1

    print("Updating Argos package index (may take a moment)...")
    argostranslate.package.update_package_index()

    available = argostranslate.package.get_available_packages()
    to_install = [
        p
        for p in available
        if p.from_code in TARGET_LANGS
        and p.to_code in TARGET_LANGS
        and p.from_code != p.to_code
    ]

    if not to_install:
        print("No packages found for en/zh/ja/de in the index. Check your network or Argos index.")
        return 1

    # De-duplicate by (from, to) in case of duplicates
    seen: set[tuple[str, str]] = set()
    unique = []
    for p in to_install:
        key = (p.from_code, p.to_code)
        if key not in seen:
            seen.add(key)
            unique.append(p)

    print(f"Found {len(unique)} package(s) to install between en, zh, ja, de.\n")

    failed: list[str] = []
    for i, pkg in enumerate(unique, 1):
        # Use ASCII "->" so Windows cp1252 consoles do not raise UnicodeEncodeError
        label = f"{pkg.from_code} -> {pkg.to_code}"
        try:
            print(f"[{i}/{len(unique)}] Downloading & installing {label}...")
            path = pkg.download()
            argostranslate.package.install_from_path(path)
            print(f"    OK: {label}")
        except Exception as e:
            print(f"    FAILED: {label} - {e}")
            failed.append(label)

    print("\n--- Summary ---")
    print(f"Installed OK: {len(unique) - len(failed)} / {len(unique)}")
    if failed:
        print("Failed:", ", ".join(failed))
        return 1

    print("\nRestart the API (uvicorn) if it is already running, then refresh the web app.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
