# TechnoPath — Fix Prompts for Kimi K2.5 (Windsurf)

> Paste any one of the prompts below into Windsurf Kimi K2.5.
> Start with **Prompt A** for a complete fix, or use individual prompts to tackle one layer at a time.

---

## Prompt A — All Issues (Full Fix)

```
You are an expert Django and Vue.js developer. Fix all errors and issues in the TechnoPath SEAIT Guide Map project. The project is a Vue 3 + Vite PWA frontend with a Django 4.2 REST API backend and a Flask chatbot service. Work through every fix below in order.

---

## CRITICAL FIXES

### Fix 1 — Remove password reset from startup script
File: `backend_django/render_start.sh`

Remove this line and its echo line above it:
  echo "Resetting all admin passwords..."
  python manage.py reset_all_passwords

This command runs on every deploy and resets all 20 admin accounts back to "admin123",
wiping any password changes made in production. Only remove these two lines — keep the rest of the file intact.

---

### Fix 2 — Remove duplicate FAQ URL registrations
File: `backend_django/technopath/urls.py`

Remove these two duplicate lines from the root urls.py (the chatbot app's own urls.py
already registers these correctly under /api/chatbot/faq/):

  path('api/faq/',            chatbot_views.FAQListView.as_view(), name='faq-list'),
  path('api/faq/<int:pk>/',   chatbot_views.FAQDetailView.as_view(), name='faq-detail'),

Also remove this import at the top if FAQListView/FAQDetailView are no longer used there:
  from apps.chatbot import views as chatbot_views

---

### Fix 3 — Add WhiteNoise to Django MIDDLEWARE and STATICFILES_STORAGE
File: `backend_django/technopath/settings.py`

WhiteNoise is in requirements.txt but never added to MIDDLEWARE. Static files will not
be served in production without this.

1. In MIDDLEWARE, add WhiteNoiseMiddleware immediately after SecurityMiddleware:
     'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',   # <-- add this line

2. After the STATIC_ROOT line, add:
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

---

## HIGH PRIORITY FIXES

### Fix 4 — Remove manual service worker registration (conflicts with vite-plugin-pwa)
File: `frontend/src/main.js`

vite-plugin-pwa already auto-generates and registers a service worker via workbox.
The manual registration below creates a conflict with two competing service workers.

Remove this entire block from main.js:
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('[SW] Registered:', reg.scope))
      .catch(err => console.warn('[SW] Registration failed:', err))
  }

Also delete the file: `frontend/public/sw.js`
vite-plugin-pwa's generated SW handles all caching via the workbox config in vite.config.js.

---

### Fix 5 — Fix env var name mismatch in .env.example
File: `frontend/.env.example`

The code in frontend/src/services/aiChatbot.js reads:
  const FLASK_CHATBOT_URL = import.meta.env.VITE_FLASK_CHATBOT_URL || '/chatbot-api'

But .env.example has the wrong variable name:
  VITE_CHATBOT_URL=http://localhost:5000   # <-- wrong name, chatbot URL is silently ignored

Change it to:
  VITE_FLASK_CHATBOT_URL=http://localhost:5000

---

### Fix 6 — Create .env files for local development
Create two new files for local development setup.

File: `backend_django/.env`
  DEBUG=True
  SECRET_KEY=dev-secret-key-change-in-production
  DATABASE_URL=
  ALLOWED_HOSTS=localhost,127.0.0.1
  CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
  FLASK_CHATBOT_URL=http://localhost:5000

File: `frontend/.env`
  VITE_API_BASE_URL=/api
  VITE_FLASK_CHATBOT_URL=http://localhost:5000
  VITE_OPENAI_API_KEY=

Add both files to .gitignore if they are not already listed.
Also update README.md to include a "Local Development Setup" section explaining that
developers must copy these files and fill in real values before running the project.

---

## MEDIUM FIXES

### Fix 7 — Fix session expiry redirect (toast never shows)
File: `frontend/src/services/api.js`

When token refresh fails, the code redirects to:
  window.location.href = '/?session_expired=1'

The router's beforeEach guard redirects / to /splash on initial load, so the
session_expired query param is never processed and the toast never shows.

Change the redirect target to:
  window.location.href = '/admin/login?session_expired=1'

---

### Fix 8 — Document PostgreSQL setup requirement
File: `render.yaml`

There is no DATABASE_URL configured. On a fresh Render deploy, Django silently falls
back to SQLite which is ephemeral — all data is lost on every redeploy.

Add this comment block under the backend service's envVars section:
  # IMPORTANT: You must manually add DATABASE_URL in the Render dashboard.
  # Create a PostgreSQL database in Render and copy its Internal Database URL here.
  # Without this, the app uses SQLite which loses ALL data on every redeploy.
  # - key: DATABASE_URL
  #   value: (set manually in Render dashboard — do not commit this value)

---

### Fix 9 — Add CORS warning for Render URL matching
File: `render.yaml`

Add a comment above CORS_ALLOWED_ORIGINS:
  # After deploying, update CORS_ALLOWED_ORIGINS in the Render dashboard to match
  # the exact URL Render assigns to your frontend service (e.g. technopath-frontend-xxxx.onrender.com).
  # Mismatched origins will silently block all API requests from the frontend.

---

## CLEANUP

### Fix 10 — Update .gitignore
File: `.gitignore` (create at repo root if it does not exist)

Add these entries:
  # Node.js installers — do not commit binaries
  *.msi
  *.zip
  node-portable*/
  node-installer*/
  nodejs*/

  # Local environment files
  .env
  backend_django/.env
  frontend/.env

  # Sensitive account files
  Acounts.txt

  # Python
  __pycache__/
  *.pyc
  *.pyo
  *.db
  staticfiles/
  media/

  # Frontend build
  frontend/dist/
  node_modules/

Note: The binary files node-installer.msi, node-portable.zip, and nodejs.msi are already
in the repo. Adding them to .gitignore prevents future re-commits, but they should also
be removed from git history using:
  git filter-repo --path node-installer.msi --invert-paths
  git filter-repo --path node-portable.zip --invert-paths
  git filter-repo --path nodejs.msi --invert-paths

### Fix 11 — Archive orphaned funtion_systems/ directory
The directory funtion_systems/ (typo — should be function_systems) contains 4.2MB of
outdated Vue component copies that are not imported anywhere in the active codebase.

Move the entire directory to _archive/funtion_systems/ so it is preserved but clearly
not part of the active project. Do not delete the files — just move them.

---

### Fix 12 — Add DRF permission class audit comment
File: `backend_django/technopath/settings.py`

The default permission class is AllowAny. Add a clear comment so future developers
understand this is intentional and know what to do when adding new endpoints.

Above DEFAULT_PERMISSION_CLASSES, add:
  # AllowAny is intentional — TechnoPath is a public-facing campus guide.
  # All read endpoints (facilities, rooms, navigation, FAQ) are open by design.
  # Admin-only endpoints must set permission_classes explicitly on the view.
  # Audit every new endpoint before deploying to ensure it is correctly protected.

---

After completing all fixes:
1. Run a syntax check on all modified Python files
2. Confirm the frontend builds without errors: cd frontend && npm run build
3. List every file you created, modified, or deleted
4. Flag any fix that required a judgment call or deviation from these instructions
```

---

## Prompt B — Critical Fixes Only

```
You are an expert Django and Vue.js developer. Fix only the 3 critical errors in the
TechnoPath SEAIT Guide Map project. These must be resolved before the app is safe to deploy.

---

### Fix 1 — Remove password reset from startup script
File: `backend_django/render_start.sh`

Remove these two lines:
  echo "Resetting all admin passwords..."
  python manage.py reset_all_passwords

This runs on every Render deploy and resets all 20 admin accounts to "admin123",
wiping any production password changes. Keep the rest of the file intact.

---

### Fix 2 — Remove duplicate FAQ URL registrations
File: `backend_django/technopath/urls.py`

Remove these two duplicate lines (the chatbot app's urls.py already registers them at /api/chatbot/faq/):
  path('api/faq/',            chatbot_views.FAQListView.as_view(), name='faq-list'),
  path('api/faq/<int:pk>/',   chatbot_views.FAQDetailView.as_view(), name='faq-detail'),

Also remove the import if it is no longer used:
  from apps.chatbot import views as chatbot_views

---

### Fix 3 — Add WhiteNoise to Django MIDDLEWARE
File: `backend_django/technopath/settings.py`

1. Add WhiteNoiseMiddleware to MIDDLEWARE directly after SecurityMiddleware:
     'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',   # <-- add this

2. Add after STATIC_ROOT:
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

After completing, verify all three modified files are syntactically valid.
```

---

## Prompt C — Backend Fixes

```
You are an expert Django developer. Fix all backend issues in the TechnoPath Django
project located in backend_django/.

---

### Fix 1 — Remove duplicate FAQ URL names
File: `backend_django/technopath/urls.py`

Remove these duplicate lines (they conflict with the same names in apps/chatbot/urls.py):
  path('api/faq/',            chatbot_views.FAQListView.as_view(), name='faq-list'),
  path('api/faq/<int:pk>/',   chatbot_views.FAQDetailView.as_view(), name='faq-detail'),

Remove the import if it is no longer needed:
  from apps.chatbot import views as chatbot_views

---

### Fix 2 — Add WhiteNoise middleware and storage backend
File: `backend_django/technopath/settings.py`

Add to MIDDLEWARE after SecurityMiddleware:
  'whitenoise.middleware.WhiteNoiseMiddleware',

Add after STATIC_ROOT:
  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

---

### Fix 3 — Create local .env file
File: `backend_django/.env` (new file)

  DEBUG=True
  SECRET_KEY=dev-secret-key-change-in-production
  DATABASE_URL=
  ALLOWED_HOSTS=localhost,127.0.0.1
  CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
  FLASK_CHATBOT_URL=http://localhost:5000

Add backend_django/.env to .gitignore.

---

### Fix 4 — Add AllowAny audit comment
File: `backend_django/technopath/settings.py`

Above DEFAULT_PERMISSION_CLASSES, add:
  # AllowAny is intentional — TechnoPath is a public campus guide.
  # Admin endpoints must set permission_classes explicitly on the view.
```

---

## Prompt D — Frontend Fixes

```
You are an expert Vue 3 / Vite developer. Fix all frontend issues in the TechnoPath
frontend located in frontend/.

---

### Fix 1 — Remove manual service worker (conflicts with vite-plugin-pwa)
File: `frontend/src/main.js`

Remove this entire block:
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('[SW] Registered:', reg.scope))
      .catch(err => console.warn('[SW] Registration failed:', err))
  }

Then delete: `frontend/public/sw.js`

vite-plugin-pwa (configured in vite.config.js) handles all service worker generation
and registration via workbox. The manual registration creates a conflict between two
competing service workers causing unpredictable caching behavior.

---

### Fix 2 — Fix env var name mismatch
File: `frontend/.env.example`

Change:
  VITE_CHATBOT_URL=http://localhost:5000

To:
  VITE_FLASK_CHATBOT_URL=http://localhost:5000

The code in src/services/aiChatbot.js reads VITE_FLASK_CHATBOT_URL. The wrong name
silently falls back to /chatbot-api with no error.

---

### Fix 3 — Create local .env file
File: `frontend/.env` (new file)

  VITE_API_BASE_URL=/api
  VITE_FLASK_CHATBOT_URL=http://localhost:5000
  VITE_OPENAI_API_KEY=

Add frontend/.env to .gitignore.

---

### Fix 4 — Fix session expiry redirect
File: `frontend/src/services/api.js`

Change:
  window.location.href = '/?session_expired=1'

To:
  window.location.href = '/admin/login?session_expired=1'

The current redirect goes to / which the router immediately sends to /splash on initial
load, swallowing the query param so the session expired toast never appears.

---

After all fixes, run: cd frontend && npm run build
Confirm it completes without errors.
```

---

## Prompt E — Deployment Fixes

```
You are an expert in Render deployments. Fix all deployment configuration issues in
the TechnoPath project.

---

### Fix 1 — Remove password reset from startup (CRITICAL)
File: `backend_django/render_start.sh`

Remove these two lines:
  echo "Resetting all admin passwords..."
  python manage.py reset_all_passwords

This runs on every Render deploy and resets all admin accounts to "admin123".
It is a critical security vulnerability — remove it immediately.

---

### Fix 2 — Document PostgreSQL requirement
File: `render.yaml`

Under the backend service envVars section, add this comment block:
  # IMPORTANT: Set DATABASE_URL manually in the Render dashboard.
  # Create a Render PostgreSQL database and paste its Internal Database URL.
  # Without it, Django uses SQLite and ALL DATA IS LOST on every redeploy.
  # - key: DATABASE_URL
  #   value: (set manually — never commit this value)

---

### Fix 3 — Add CORS URL warning
File: `render.yaml`

Above CORS_ALLOWED_ORIGINS, add:
  # After deploying, update CORS_ALLOWED_ORIGINS in the Render dashboard
  # to match the exact auto-generated frontend URL (e.g. technopath-frontend-xxxx.onrender.com).
  # Mismatched origins silently block all frontend API requests.
```

---

## Prompt F — Cleanup Tasks

```
You are a developer doing repository cleanup on the TechnoPath project.
Complete all cleanup tasks below.

---

### Task 1 — Create or update .gitignore
File: `.gitignore` at repo root

Add these entries if not already present:
  # Node.js installers
  *.msi
  *.zip
  node-portable*/
  node-installer*/

  # Local environment files
  .env
  backend_django/.env
  frontend/.env

  # Sensitive files
  Acounts.txt

  # Python
  __pycache__/
  *.pyc
  *.pyo
  *.db
  staticfiles/
  media/

  # Frontend build
  frontend/dist/
  node_modules/

---

### Task 2 — Archive orphaned funtion_systems/ directory
The directory funtion_systems/ (note typo) contains 4.2MB of outdated Vue component
copies not imported anywhere in the active codebase.

Move the entire funtion_systems/ directory to _archive/funtion_systems/.
Do not delete files — only move them.

---

### Task 3 — Review and handle Acounts.txt
Open and read Acounts.txt. If it contains real usernames, passwords, or credentials:
1. Report what you find (do not display actual passwords)
2. Remove the file from the working directory
3. Confirm it is in .gitignore

If it contains only dummy/placeholder data, move it to _archive/Acounts.txt.

---

### Task 4 — Add README local development setup section
File: `README.md`

Add a "Local Development Setup" section with these steps:
  1. Clone the repository
  2. Copy backend_django/.env.example to backend_django/.env and fill in values
  3. Copy frontend/.env.example to frontend/.env and fill in values
  4. cd backend_django && pip install -r requirements.txt
  5. python manage.py migrate
  6. python manage.py seed_default_data
  7. python manage.py runserver
  8. cd frontend && npm install
  9. npm run dev

Add this warning at the bottom of the section:
  > Warning: node-installer.msi, node-portable.zip, and nodejs.msi should be removed
  > from git history. Use git filter-repo --path <filename> --invert-paths for each.
```

---

## Issue Reference

| # | Severity | Issue | File |
|---|----------|-------|------|
| 1 | Critical | Passwords reset to `admin123` on every deploy | `render_start.sh` |
| 2 | Critical | Duplicate FAQ URL names cause `NoReverseMatch` | `urls.py` + `chatbot/urls.py` |
| 3 | Critical | WhiteNoise missing from MIDDLEWARE — static files broken in prod | `settings.py` |
| 4 | High | Double service worker registration conflict | `main.js` + `vite.config.js` |
| 5 | High | Missing local `.env` files — undocumented dev setup | repo root |
| 6 | High | Env var mismatch: `VITE_CHATBOT_URL` vs `VITE_FLASK_CHATBOT_URL` | `.env.example` |
| 7 | Medium | Session expiry redirect loops through splash — toast never shows | `api.js` |
| 8 | Medium | No PostgreSQL linked in `render.yaml` — SQLite used in production | `render.yaml` |
| 9 | Medium | CORS origins may not match actual Render-assigned URLs | `render.yaml` |
| 10 | Medium | `funtion_systems/` is 4.2MB of orphaned duplicate Vue files | repo root |
| 11 | Medium | 81MB of Node.js installer binaries committed to Git | repo root |
| 12 | Minor | `Acounts.txt` may contain sensitive account data | repo root |
| 13 | Minor | `AllowAny` as default DRF permission class — needs audit comment | `settings.py` |
