/**
 * Download link for the translated file. Opens in same tab so the file downloads.
 */
import { getDownloadUrl } from '../api/client'

interface DownloadLinkProps {
  jobId: string
  filename: string | null
}

export function DownloadLink({ jobId, filename }: DownloadLinkProps) {
  const url = getDownloadUrl(jobId)
  const label = filename ? `Download ${filename}` : 'Download translated file'

  return (
    <a
      href={url}
      className="btn btn-primary download-link"
      download={filename ?? undefined}
      rel="noopener noreferrer"
    >
      {label}
    </a>
  )
}
