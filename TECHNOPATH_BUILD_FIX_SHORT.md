# TechnoPath — Render Build Fix

## Error
`pathManager.js (520:0): Failed to parse source for import analysis — invalid JS syntax`

## Root Cause
Previous AI session made 3 bad changes. Fix all 3.

---

## Fix 1 — `frontend/package.json`
Remove `"type": "module"` — this line breaks Rollup's parser on class syntax.

---

## Fix 2 — `frontend/vite.config.js`
Replace entire file with this:

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: 'script',
      workbox: {
        cleanupOutdatedCaches: true,
        skipWaiting: true,
        clientsClaim: true,
        globPatterns: ['**/*.{js,css,html,svg,png,jpg}'],
        globIgnores: ['**/sw.js', '**/workbox-*.js', '**/registerSW.js'],
        runtimeCaching: [{
          urlPattern: ({ url }) => url.pathname.startsWith('/api/'),
          handler: 'NetworkFirst',
          options: { cacheName: 'api-cache', expiration: { maxEntries: 100, maxAgeSeconds: 86400 } }
        }]
      },
      manifest: {
        name: 'TechnoPath SEAIT Guide',
        short_name: 'TechnoPath',
        theme_color: '#FF9800',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: './',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      }
    })
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/chatbot-api': { target: 'http://localhost:5187', changeOrigin: true, rewrite: (p) => p.replace(/^\/chatbot-api/, '') }
    }
  }
})
```

---

## Fix 3 — `render.yaml`
Find and remove this line under backend envVars:
```
value: sqlite:///tmp/technopath.db
```
Replace with:
```yaml
# Set DATABASE_URL manually in Render dashboard (PostgreSQL). Never use sqlite:///tmp/
```

## Fix 4 — Delete these files if they exist
- `frontend/public/sw.js`
- `frontend/public/manifest.json`

---

## Verify
```bash
cd frontend && rm -rf dist node_modules/.vite && npm install && npm run build
```
Must complete with no errors before pushing.
