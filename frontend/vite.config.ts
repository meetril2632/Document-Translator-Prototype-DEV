import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite config: React plugin and API proxy (optional) to backend.
 * Frontend uses VITE_API_URL for the API base (default http://localhost:8000).
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Allow other devices on your home Wi-Fi to access the dev server
    // via http://<this-laptop-ip>:5173/
    host: true,
    proxy: {
      // Optional: proxy /api to backend so we don't need CORS in dev
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
