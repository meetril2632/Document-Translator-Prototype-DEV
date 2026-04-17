# Document Translator

Upload documents (Word, Excel, CSV, Text), translate them **offline** using Argos Translate, and download the result with format preserved. Content never leaves your server.

## Tech Stack

- **Frontend:** React 18 + Vite (TypeScript)
- **Backend:** FastAPI (Python)
- **Translation:** Argos Translate (offline; no Google/DeepL API)

## Project structure

```
translator_webapp/
├── backend/                 # FastAPI app
│   ├── app/
│   │   ├── main.py         # App entry, CORS, routes
│   │   ├── config.py       # Settings from env
│   │   ├── routers/       # upload, languages, translate, download
│   │   ├── schemas/        # Pydantic request/response models
│   │   └── services/
│   │       ├── translation.py   # Argos Translate wrapper
│   │       ├── pipeline.py      # extract → translate → rebuild
│   │       ├── extractors/      # CSV, DOCX text extraction
│   │       └── rebuild/         # CSV, DOCX rebuild
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React + Vite
│   ├── src/
│   │   ├── api/client.ts   # API client
│   │   ├── components/     # UploadZone, LanguagePicker, Progress, DownloadLink
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── vite.config.ts      # React plugin + optional /api proxy
│   └── .env.example
└── README.md
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Install offline language packs. **Recommended:** English, Chinese, Japanese, and German (all pairs Argos provides between these four):

```bash
# From the backend folder, with venv activated (run once; downloads several hundred MB)
python scripts/install_language_packs.py
```

On Windows you can also double-click `backend/install_packs.bat` (same script, uses `venv` in that folder).

**Optional — single pair** (e.g. English → Spanish only):

```bash
python -c "import argostranslate.package as p; p.update_package_index(); pkgs = p.get_available_packages(); pkg = next(x for x in pkgs if x.from_code == 'en' and x.to_code == 'es'); p.install_from_path(pkg.download()); print('Installed en -> es')"
```

After installing packs, **restart** `uvicorn` and refresh the web app.

Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 . The Vite dev server proxies `/api` to the backend, so no CORS issues in development.

### 3. Use the app

1. Upload a file (CSV, DOCX, XLSX, or TXT supported in this version).
2. Choose source and target language (from installed Argos pairs).
3. Click **Translate**.
4. Download the translated file — the **download filename** uses the same translation (stem translated, extension unchanged), e.g. `Monthly Report.docx` → `月度报告.docx` when translating to Chinese.

## Configuration

- **Backend:** Copy `backend/.env.example` to `backend/.env`. Options: `MAX_FILE_SIZE`, `TEMP_DIR`, `CORS_ORIGINS`.
- **Frontend:** For a production build, set `VITE_API_URL` to your backend URL (e.g. `https://api.example.com`) in `frontend/.env.local`.

## Supported formats

| Format | Extract | Rebuild | Status   |
|--------|---------|---------|----------|
| CSV    | ✅      | ✅      | Supported |
| DOCX   | ✅      | ✅      | Supported |
| XLSX   | ✅      | ✅      | Supported |
| TXT    | ✅      | ✅      | Supported |

## Documentation in code

- Backend: docstrings on modules and functions; type hints throughout.
- Frontend: JSDoc-style comments on API client and components.
- Routers and services are split so you can debug and test each step (upload → extract → translate → rebuild → download) separately.

## License

Use as you like. Argos Translate has its own license (see PyPI).
