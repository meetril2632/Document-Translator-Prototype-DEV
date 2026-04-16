/**
 * Source and target language dropdowns from installed Argos pairs.
 * If no packs are installed, shows OfflineLanguageSetup instructions.
 */

import { OfflineLanguageSetup } from './OfflineLanguageSetup'

/** Friendly labels for common ISO codes (Argos uses short codes like en, zh, ja, de). */
const LANGUAGE_LABELS: Record<string, string> = {
  en: 'English',
  zh: 'Chinese',
  ja: 'Japanese',
  de: 'German',
  es: 'Spanish',
  fr: 'French',
  ru: 'Russian',
  ko: 'Korean',
  pt: 'Portuguese',
  it: 'Italian',
}

function labelFor(code: string): string {
  return LANGUAGE_LABELS[code] ? `${LANGUAGE_LABELS[code]} (${code})` : code.toUpperCase()
}

interface LanguagePickerProps {
  pairs: { source: string; target: string; source_name?: string; target_name?: string }[]
  sourceLang: string
  targetLang: string
  onSourceChange: (code: string) => void
  onTargetChange: (code: string) => void
}

export function LanguagePicker({
  pairs,
  sourceLang,
  targetLang,
  onSourceChange,
  onTargetChange,
}: LanguagePickerProps) {
  const sources = Array.from(new Set(pairs.map((p) => p.source))).sort()
  const targetsForSource = Array.from(
    new Set(pairs.filter((p) => p.source === sourceLang).map((p) => p.target))
  ).sort()
  const hasPairs = pairs.length > 0

  return (
    <div className="language-picker-wrap">
      {!hasPairs && <OfflineLanguageSetup />}
      <div className="language-picker">
        <label className="picker-label">
          Source language
          <select
            value={hasPairs && sources.includes(sourceLang) ? sourceLang : ''}
            onChange={(e) => onSourceChange(e.target.value)}
            disabled={!hasPairs}
            aria-label="Source language"
          >
            {sources.length === 0 && <option value="">— No packs —</option>}
            {sources.map((code) => (
              <option key={code} value={code}>
                {labelFor(code)}
              </option>
            ))}
          </select>
        </label>
        <label className="picker-label">
          Target language
          <select
            value={hasPairs && targetsForSource.includes(targetLang) ? targetLang : ''}
            onChange={(e) => onTargetChange(e.target.value)}
            disabled={!hasPairs || targetsForSource.length === 0}
            aria-label="Target language"
          >
            {targetsForSource.length === 0 && <option value="">— No direction —</option>}
            {targetsForSource.map((code) => (
              <option key={code} value={code}>
                {labelFor(code)}
              </option>
            ))}
          </select>
        </label>
      </div>
      {hasPairs && (
        <p className="language-picker-note" role="note">
          Only installed offline translation directions are listed. Direct cross-language translation (for
          example Chinese to Japanese, or Japanese to German) is not available here as of now.
        </p>
      )}
    </div>
  )
}
