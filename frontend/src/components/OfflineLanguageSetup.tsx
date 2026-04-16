/**
 * One-time Argos offline model install instructions (English, Chinese, Japanese, German).
 * Option B: terminal only (see README for Windows .bat alternative if needed).
 */
export function OfflineLanguageSetup() {
  return (
    <details className="language-picker-help" open>
      <summary className="language-picker-help-summary">
        One-time setup: install offline languages (English, Chinese, Japanese, German)
      </summary>
      <div className="language-picker-help-body">
        <p className="language-picker-help-text">
          Translation runs on your PC. Install Argos models once, then restart the API and refresh
          this page.
        </p>
        <p className="language-picker-help-text">
          <strong>Terminal (Option B):</strong> open a terminal in the <strong>backend</strong> folder
          with your Python venv activated, then run:
        </p>
        <pre className="language-picker-help-code">python scripts\install_language_packs.py</pre>
        <p className="language-picker-help-text language-picker-help-foot">
          Downloads are large (several hundred MB). After install: stop and start uvicorn, then refresh
          here.
        </p>
      </div>
    </details>
  )
}
