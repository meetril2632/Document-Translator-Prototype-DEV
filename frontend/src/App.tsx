/**
 * Main app: upload → language selection → translate → download.
 * Single-page flow with step-wise feedback.
 */
import { useState, useCallback, useEffect, useLayoutEffect } from 'react'
import { uploadFile, getLanguages, translateDocument, checkBackendHealth } from './api/client'
import type { LanguagePair } from './api/client'
import { BackendBanner } from './components/BackendBanner'
import { UploadZone } from './components/UploadZone'
import { LanguagePicker } from './components/LanguagePicker'
import { OfflineLanguageSetup } from './components/OfflineLanguageSetup'
import { Progress } from './components/Progress'
import { DownloadLink } from './components/DownloadLink'

type ThemeMode = 'light' | 'dark' | 'system'

export default function App() {
  const [jobId, setJobId] = useState<string | null>(null)
  const [filename, setFilename] = useState<string | null>(null)
  const [pairs, setPairs] = useState<LanguagePair[]>([])
  const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('en')
  const [step, setStep] = useState<'idle' | 'uploading' | 'uploaded' | 'translating' | 'done' | 'error'>('idle')
  const [error, setError] = useState<string | null>(null)
  const [translatedFilename, setTranslatedFilename] = useState<string | null>(null)
  /** True when FastAPI is not running — Vite shows "Bad Gateway" for uploads in that case. */
  const [backendDown, setBackendDown] = useState<boolean | null>(null)
  /** After first health + language fetch, hide the startup message. */
  const [appReady, setAppReady] = useState(false)
  const [themeMode, setThemeMode] = useState<ThemeMode>('system')

  const currentStage = step === 'done'
    ? 4
    : step === 'translating'
      ? 3
      : step === 'uploaded' || step === 'uploading'
        ? 2
        : 1

  // Load all installed Argos pairs (bidirectional — whatever the backend reports).
  const loadLanguages = useCallback(async () => {
    try {
      const res = await getLanguages()
      const list = res.pairs || []
      setPairs(list)
    } catch (e) {
      console.warn('Could not load languages:', e)
      setPairs([])
    }
  }, [])

  const recheckBackend = useCallback(async () => {
    const ok = await checkBackendHealth()
    setBackendDown(!ok)
    if (ok) await loadLanguages()
  }, [loadLanguages])

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const ok = await checkBackendHealth()
        if (!cancelled) setBackendDown(!ok)
        await loadLanguages()
      } finally {
        if (!cancelled) setAppReady(true)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [loadLanguages])

  /** Keep source/target aligned with installed pairs (valid direction only). */
  useLayoutEffect(() => {
    if (pairs.length === 0) return
    const outgoing = pairs.filter((p) => p.source === sourceLang)
    if (outgoing.length === 0) {
      const p0 = pairs[0]
      setSourceLang(p0.source)
      setTargetLang(p0.target)
      return
    }
    setTargetLang((t) =>
      outgoing.some((p) => p.target === t)
        ? t
        : [...new Set(outgoing.map((p) => p.target))].sort()[0]
    )
  }, [pairs, sourceLang])

  useEffect(() => {
    const saved = localStorage.getItem('translator-theme')
    if (saved === 'light' || saved === 'dark' || saved === 'system') {
      setThemeMode(saved)
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('translator-theme', themeMode)
    const root = document.documentElement
    if (themeMode === 'system') {
      root.removeAttribute('data-theme')
    } else {
      root.setAttribute('data-theme', themeMode)
    }
  }, [themeMode])

  const handleUpload = useCallback(async (file: File) => {
    setError(null)
    setStep('uploading')
    try {
      const res = await uploadFile(file)
      setJobId(res.job_id)
      setFilename(res.filename)
      setStep('uploaded')
      if (!pairs.length) await loadLanguages()
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e)
      setError(message)
      setStep('error')
    }
  }, [pairs.length, loadLanguages])

  const handleTranslate = useCallback(async () => {
    if (!jobId) return
    setError(null)
    setStep('translating')
    try {
      const res = await translateDocument(jobId, sourceLang, targetLang)
      setTranslatedFilename(res.translated_filename || null)
      setStep('done')
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : String(e)
      setError(message)
      setStep('error')
    }
  }, [jobId, sourceLang, targetLang])

  const handleReset = useCallback(() => {
    setJobId(null)
    setFilename(null)
    setStep('idle')
    setError(null)
    setTranslatedFilename(null)
  }, [])

  return (
    <div className="app-shell">
      <div className="bg-orb bg-orb-1" aria-hidden />
      <div className="bg-orb bg-orb-2" aria-hidden />
      <div className="bg-grid" aria-hidden />

      <div className="app">
        <header className="app-header">
          <div className="app-header-top">
            <div className="app-badge">Offline • Private • Fast</div>
            <div className="theme-switch" role="group" aria-label="Theme switcher">
              <button type="button" className={`theme-btn ${themeMode === 'light' ? 'active' : ''}`} onClick={() => setThemeMode('light')}>Light</button>
              <button type="button" className={`theme-btn ${themeMode === 'dark' ? 'active' : ''}`} onClick={() => setThemeMode('dark')}>Dark</button>
              <button type="button" className={`theme-btn ${themeMode === 'system' ? 'active' : ''}`} onClick={() => setThemeMode('system')}>Auto</button>
            </div>
          </div>
          <h1>Document Translator</h1>
          <p className="subtitle">Upload a file, choose languages, translate offline. Your content never leaves this server.</p>
        </header>

        {backendDown === true && appReady && <BackendBanner onRetry={recheckBackend} />}

        <main className="app-main">
        <aside className="step-rail" aria-label="Translation steps">
          <div className={`step-item ${currentStage >= 1 ? 'done' : ''}`}>
            <span className="step-dot">1</span>
            <div><p>Upload</p><small>Select source file</small></div>
          </div>
          <div className={`step-item ${currentStage >= 2 ? 'done' : ''}`}>
            <span className="step-dot">2</span>
            <div><p>Language</p><small>Choose source and target</small></div>
          </div>
          <div className={`step-item ${currentStage >= 3 ? 'done' : ''}`}>
            <span className="step-dot">3</span>
            <div><p>Translate</p><small>Offline processing</small></div>
          </div>
          <div className={`step-item ${currentStage >= 4 ? 'done' : ''}`}>
            <span className="step-dot">4</span>
            <div><p>Download</p><small>Get translated file</small></div>
          </div>
        </aside>
        <section className={`content-panel state-${step}`}>
        {!appReady && (
          <div className="app-startup" role="status" aria-live="polite" aria-busy="true">
            <div className="app-startup-spinner" aria-hidden />
            <p className="app-startup-text">Connecting to translation server…</p>
            <p className="app-startup-hint">If this takes long, start the backend: <code>uvicorn app.main:app --reload --port 8000</code></p>
          </div>
        )}

        {appReady && step === 'idle' && pairs.length === 0 && <OfflineLanguageSetup />}

        {appReady && step === 'idle' && (
          <UploadZone onUpload={handleUpload} disabled={false} />
        )}

        {appReady && (step === 'uploading' || step === 'uploaded') && (
          <>
            <Progress stage={step === 'uploading' ? 'uploading' : 'uploaded'} filename={filename ?? undefined} />
            <LanguagePicker
              pairs={pairs}
              sourceLang={sourceLang}
              targetLang={targetLang}
              onSourceChange={setSourceLang}
              onTargetChange={setTargetLang}
            />
            <div className="actions">
              <button type="button" className="btn btn-primary" onClick={handleTranslate} disabled={!jobId || pairs.length === 0}>
                Translate
              </button>
              <button type="button" className="btn btn-secondary" onClick={handleReset}>Cancel</button>
            </div>
          </>
        )}

        {appReady && step === 'translating' && (
          <Progress stage="translating" />
        )}

        {appReady && step === 'done' && jobId && (
          <>
            <Progress stage="done" filename={translatedFilename ?? undefined} />
            <DownloadLink jobId={jobId} filename={translatedFilename} />
            <button type="button" className="btn btn-secondary" onClick={handleReset}>Translate another</button>
          </>
        )}

        {appReady && step === 'error' && (
          <>
            <div className="error-box" role="alert">
              {error}
            </div>
            <button type="button" className="btn btn-primary" onClick={() => setStep('idle')}>Try again</button>
          </>
        )}
        </section>
        </main>

        <footer className="app-footer">
          <p>Accepted: Word (.docx), Excel (.xlsx), CSV, Text (.txt). Max 10 MB. Files are deleted after download.</p>
        </footer>
      </div>
    </div>
  )
}
