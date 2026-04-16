# How to Start the Document Translator

Follow these steps **in order**. You need **Python 3.10+** and **Node.js (npm)** installed.

---

## Step 1: Start the backend (FastAPI)

Open a terminal (PowerShell or Command Prompt) and run:

```powershell
cd ..\Document-Translator-Prototype-DEV\backend

# Create a virtual environment (first time only)
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt
```

**Install offline language packs** (first time only — English, Chinese, Japanese, German):

```powershell
python scripts\install_language_packs.py
```

This downloads **several hundred MB** (one model per direction Argos offers between `en`, `zh`, `ja`, `de`). When it finishes, continue below.

**Start the API server:**

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Leave this terminal open. You should see something like:

```
Uvicorn running on http://0.0.0.0:8000
```

- API docs: **http://localhost:8000/docs**
- Health check: **http://localhost:8000/**

---

## Step 2: Start the frontend (React)

Open a **second** terminal and run:

```powershell
cd ..\Document-Translator-Prototype-DEV\frontend

# Install dependencies (first time only)
npm install

# Start the dev server
npm run dev
```

Leave this terminal open. You should see something like:

```
  VITE ready in ... ms
  Local:   http://localhost:5173/
```

---

## Step 3 (LAN): Other devices on the same Wi‑Fi

If you want friends/other devices on the **same home Wi‑Fi** to use the app:

1. Find your laptop IPv4 address:

```powershell
ipconfig
```

Look for `IPv4 Address` (example: `192.168.1.50`).

2. Open this URL from the other device:

`http://<YOUR_LAPTOP_IP>:5173/`

Example:
`http://192.168.1.50:5173/`

3. Ensure Windows Firewall allows inbound access to:
   - `5173/TCP` (Vite frontend)
   - `8000/TCP` (FastAPI backend)

---

## Step 4: Use the app

1. Open your browser and go to: **http://localhost:5173**
2. **Upload** a file (CSV, XLSX, DOCX, or TXT — max 10 MB).
3. Choose **Source language** and **Target language** (from the dropdowns).
4. Click **Translate** and wait for “Translation complete.”
5. Click **Download** to save the translated file.

---

## Troubleshooting

| Problem | What to do |
|--------|------------|
| `python` not found | Install Python from python.org and ensure “Add to PATH” is checked. Use `py -m venv venv` if you have the Python launcher. |
| `uvicorn` not found | Make sure the venv is activated (`.\venv\Scripts\activate`) and run `pip install -r requirements.txt` again. |
| `npm` not found | Install Node.js from nodejs.org (LTS). |
| Language dropdowns empty | Run the “Install a language pack” command in Step 1 (en → es). |
| “Job not found” or 404 on download | Translate first, then download. Don’t refresh the page between translate and download. |
| CORS errors in browser | Ensure the backend is running on port 8000 and the frontend on 5173. The frontend proxies `/api` to the backend. |
| **Bad Gateway** when uploading (.docx, etc.) | The FastAPI server is **not running** or not on port **8000**. Vite’s proxy returns 502. Start the backend (Step 1), wait until you see “Uvicorn running”, then refresh the app. |

---

## Quick reference

| What | URL or command |
|------|----------------|
| Open the app | http://localhost:5173 |
| Backend API docs | http://localhost:8000/docs |
| Backend (activate + run) | `cd backend` → `.\venv\Scripts\activate` → `uvicorn app.main:app --reload --port 8000` |
| Frontend (run) | `cd frontend` → `npm run dev` |
