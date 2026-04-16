/**
 * Shown when /api/health fails — usually FastAPI is not running on port 8000.
 * "Bad Gateway" from Vite means the proxy could not reach the backend.
 */
import { BACKEND_OFFLINE_MESSAGE } from '../api/client'

interface BackendBannerProps {
  onRetry: () => void
}

export function BackendBanner({ onRetry }: BackendBannerProps) {
  return (
    <div className="backend-banner" role="alert">
      <p className="backend-banner-title">Backend not reachable</p>
      <p className="backend-banner-text">{BACKEND_OFFLINE_MESSAGE}</p>
      <button type="button" className="btn btn-secondary backend-banner-retry" onClick={onRetry}>
        Check again
      </button>
    </div>
  )
}
