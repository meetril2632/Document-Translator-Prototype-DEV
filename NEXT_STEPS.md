# Session Resume Guide

This file is the **project memory** for the Document Translator Prototype DEV Web app. Cursor does not copy full chat transcripts into your disk automatically; keeping this file updated and reopening this folder is how you reliably resume.

## When you start a different project in a new folder

Nothing here is deleted. To come back to **this** project later:

1. In Cursor: **File → Open Folder** and choose:
   - `..\Document-Translator-Prototype-DEV`
2. Open `NEXT_STEPS.md` (this file).
3. In a new chat, paste something like:
   - `Read NEXT_STEPS.md and continue the Document Translator Prototype DEV work from there.`

Optional: add this folder to **File → Add Folder to Workspace** or pin it in your recent folders so it is easy to find.

Chat history may still appear in Cursor for the same account, but **do not rely on it alone**—this file + the same workspace path is the durable handoff.

## Reopen Context Checklist (quick)

1. Open workspace: `..\Document-Translator-Prototype-DEV`
2. Open: `NEXT_STEPS.md`
3. In chat: `Continue from NEXT_STEPS.md in this workspace.`

## Current Project State

- Stack:
  - Frontend: React + Vite
  - Backend: FastAPI + Argos Translate
- Accepted upload types:
  - `.xlsx`, `.csv`, `.docx`, `.txt`
- Implemented features:
  - Offline translation flow (local Argos models)
  - DOCX header/footer translation traversal
  - XLSX/TXT extraction and rebuild
  - Filename translation for output download name
  - LAN-ready frontend host config (`vite` host enabled)
  - UI redesign + theme switch + step rail
- Language workflow currently constrained in UI:
  - Source: `zh`, `ja`, `de` (installed pairs only)
  - Target fixed to `en`

## Important Runtime Notes

- Start backend:
  - `cd backend`
  - `.\venv\Scripts\activate`
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Start frontend:
  - `cd frontend`
  - `npm run dev`
- LAN URL for other devices:
  - `http://<your-laptop-ip>:5173`

## Pending Security Work (Not Yet Implemented)

Goal: strict guarantee that uploaded data never leaves this computer, even when internet is ON.

Planned:
1. App strict mode flag (`STRICT_LOCAL_MODE=true`)
2. Startup preflight checks for offline-only safety
3. Windows firewall outbound block for backend Python process (with rollback commands)
4. Health endpoint should expose strict mode status

## Resume Prompt (copy/paste)

`Continue from NEXT_STEPS.md. Next task: implement strict local mode + firewall guidance, with fail-closed behavior and explicit diagnostics.`

