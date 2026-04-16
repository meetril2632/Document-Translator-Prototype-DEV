/**
 * Drag-and-drop and file input for uploading a document.
 */
import { useCallback, useRef } from 'react'

interface UploadZoneProps {
  onUpload: (file: File) => void
  disabled?: boolean
}

const ACCEPT = '.docx,.xlsx,.csv,.txt'
const MAX_MB = 10

function validateFile(file: File): string | null {
  const ext = '.' + (file.name.split('.').pop() || '').toLowerCase()
  const allowed = ['.docx', '.xlsx', '.csv', '.txt']
  if (!allowed.includes(ext)) {
    return `File type not allowed. Accepted: ${allowed.join(', ')}`
  }
  if (file.size > MAX_MB * 1024 * 1024) {
    return `File too large. Max size: ${MAX_MB} MB`
  }
  return null
}

export function UploadZone({ onUpload, disabled }: UploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = useCallback(
    (file: File | null) => {
      if (!file || disabled) return
      const err = validateFile(file)
      if (err) {
        alert(err)
        return
      }
      onUpload(file)
    },
    [onUpload, disabled]
  )

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      const file = e.dataTransfer.files[0]
      handleFile(file || null)
    },
    [handleFile]
  )

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
  }, [])

  const onInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      handleFile(e.target.files?.[0] ?? null)
      e.target.value = ''
    },
    [handleFile]
  )

  return (
    <div
      className="upload-zone"
      onDrop={onDrop}
      onDragOver={onDragOver}
      role="button"
      tabIndex={0}
      onClick={() => inputRef.current?.click()}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          inputRef.current?.click()
        }
      }}
      aria-label="Upload file for translation"
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        onChange={onInputChange}
        disabled={disabled}
        className="upload-input"
        aria-hidden
      />
      <p className="upload-prompt">Drop a file here or click to browse</p>
      <p className="upload-hint">Word (.docx), Excel (.xlsx), CSV, Text (.txt) — max {MAX_MB} MB</p>
    </div>
  )
}
