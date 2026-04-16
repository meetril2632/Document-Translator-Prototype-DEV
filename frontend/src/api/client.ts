/**

 * API client for the translation backend.

 * Uses VITE_API_URL in production; in dev with proxy we use relative /api.

 */



const API_BASE = import.meta.env.VITE_API_URL ?? ''



/** Shown when Vite proxy returns 502 (backend not running on port 8000). */

export const BACKEND_OFFLINE_MESSAGE =

  'Translation server is not running. Open a terminal, go to the backend folder, activate the venv, then run: uvicorn app.main:app --reload --port 8000'



export interface UploadResponse {

  job_id: string

  filename: string

}



export interface LanguagePair {

  source: string

  target: string

  source_name?: string

  target_name?: string

}



export interface LanguagesResponse {

  pairs: LanguagePair[]

  languages: string[]

}



export interface TranslateResponse {

  job_id: string

  status: string

  translated_filename?: string

  message?: string

}



function friendlyHttpError(res: Response, text: string): string {

  if (res.status === 502 || res.status === 503) {

    return BACKEND_OFFLINE_MESSAGE

  }

  if (res.status === 504) {

    return 'The server took too long to respond. Is the backend running?'

  }

  try {

    const j = JSON.parse(text)

    const detail = j.detail

    if (Array.isArray(detail)) {

      return detail.map((d: { msg?: string }) => d.msg).join(', ') || text || res.statusText

    }

    if (typeof detail === 'string') {

      return detail

    }

  } catch {

    /* use text below */

  }

  return text?.trim() || res.statusText || `Request failed (${res.status})`

}



async function handleResponse<T>(res: Response): Promise<T> {

  if (!res.ok) {

    const text = await res.text()

    throw new Error(friendlyHttpError(res, text))

  }

  return res.json() as Promise<T>

}



async function fetchWithBackendHint(url: string, init?: RequestInit): Promise<Response> {

  try {

    return await fetch(url, init)

  } catch (e) {

    // Network error (no connection, CORS in prod, etc.)

    if (e instanceof TypeError) {

      throw new Error(BACKEND_OFFLINE_MESSAGE)

    }

    throw e

  }

}



/**

 * True if the FastAPI backend answers (useful before upload).

 */

export async function checkBackendHealth(): Promise<boolean> {

  try {

    const res = await fetchWithBackendHint(`${API_BASE}/api/health`)

    return res.ok

  } catch {

    return false

  }

}



/**

 * Upload a file. Returns job_id and filename.

 */

export async function uploadFile(file: File): Promise<UploadResponse> {

  const form = new FormData()

  form.append('file', file)

  const res = await fetchWithBackendHint(`${API_BASE}/api/upload`, {

    method: 'POST',

    body: form,

  })

  return handleResponse<UploadResponse>(res)

}



/**

 * Fetch installed language pairs from Argos.

 */

export async function getLanguages(): Promise<LanguagesResponse> {

  const res = await fetchWithBackendHint(`${API_BASE}/api/languages`)

  return handleResponse<LanguagesResponse>(res)

}



/**

 * Start translation for an uploaded file.

 */

export async function translateDocument(

  jobId: string,

  sourceLang: string,

  targetLang: string

): Promise<TranslateResponse> {

  const res = await fetchWithBackendHint(`${API_BASE}/api/translate`, {

    method: 'POST',

    headers: { 'Content-Type': 'application/json' },

    body: JSON.stringify({

      job_id: jobId,

      source_lang: sourceLang,

      target_lang: targetLang,

    }),

  })

  return handleResponse<TranslateResponse>(res)

}



/**

 * Return the URL to download the translated file (for use in <a download> or fetch).

 */

export function getDownloadUrl(jobId: string): string {

  return `${API_BASE}/api/download/${encodeURIComponent(jobId)}`

}


