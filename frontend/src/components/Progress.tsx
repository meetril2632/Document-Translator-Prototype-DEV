/**
 * Step-wise progress message: uploading → uploaded → translating → done.
 */
interface ProgressProps {
  stage: 'uploading' | 'uploaded' | 'translating' | 'done'
  filename?: string
}

const messages: Record<string, string> = {
  uploading: 'Uploading…',
  uploaded: 'File uploaded. Choose languages and click Translate.',
  translating: 'Extracting, translating, and rebuilding…',
  done: 'Translation complete. Download your file below.',
}

export function Progress({ stage, filename }: ProgressProps) {
  const msg = messages[stage] ?? stage
  return (
    <div className="progress" role="status" aria-live="polite">
      <p className="progress-message">{msg}</p>
      {filename && <p className="progress-filename">{filename}</p>}
    </div>
  )
}
