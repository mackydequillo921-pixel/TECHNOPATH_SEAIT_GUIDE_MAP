# TechnoPath — AdminPathManager Cross-Device Data Fix
### Prompt for Windsurf Kimi K2.5

---

## The Problem

AdminPathManager data is **not visible on other devices** because the system has two
separate storage layers that are not properly in sync:

1. **`localStorage`** — browser-local storage, device-specific. Data saved here is
   invisible to any other device, browser, or user.
2. **Django database (PostgreSQL)** — the real shared backend that all devices read from.

The current code was designed to use the API as primary storage, but has multiple bugs
that cause it to silently fall back to localStorage instead of persisting to the database.
This means paths created on Device A are saved to Device A's localStorage only and never
reach the database — so Device B sees nothing.

There are **4 specific bugs** causing this. Fix all of them.

---

## Root Cause Analysis

### Bug 1 — `visualPoints` are never sent to the API (data is lost on save)

**File:** `frontend/src/services/pathManager.js` — `toApiFormat()` method

The `toApiFormat()` function converts the internal path object to the API payload.
It sends `points_input` and `element_ids`, but **`points_input` is set to
`pathData.points`**, which is the raw `[x, y]` coordinate array. However, in
`createPath()`, the `points` variable is built as:

```js
const points = pathData.points || pathData.visualPoints?.map(p => [p.x, p.y]) || []
```

When `pathData.points` is already a pre-built array of `[x, y]` pairs (set in
`savePath()` in AdminPathManager.vue), the coordinates **are** being sent correctly.

However the real issue is in the **fallback logic**: if the API call fails for any
reason (network blip, cold start on Render free tier, auth token expiry), the code
catches the error and silently saves to localStorage only:

```js
} catch (error) {
  console.warn('API failed, saving to localStorage:', error)
  this.useApi.value = false   // <-- permanently disables API for the session!
  // saves to localStorage only from this point on
}
```

Once `useApi` is set to `false`, **all subsequent saves in that session go to
localStorage only**, even if the API recovers. This means one failed request
permanently breaks cross-device sync for the entire session.

**Fix:** Remove the `this.useApi.value = false` line from the catch block in
`createPath()`. Do NOT permanently disable the API on a single failure. Instead,
log the error and re-throw it so the UI can show the user a real error message.
The localStorage fallback should only be used when the app is intentionally offline,
not on any API error.

---

### Bug 2 — `updatePath()` silently skips the API for paths with numeric-looking IDs

**File:** `frontend/src/services/pathManager.js` — `updatePath()` method

The code checks if a path ID looks like a localStorage-generated ID:

```js
const isLocalPath = id.startsWith('path_') && /path_\d+/.test(id)
if (!isLocalPath) {
  // try API
} else {
  // localStorage only — no API call at all
}
```

The problem: Django's database assigns **integer IDs** (1, 2, 3...). When a path is
fetched from the API and stored in memory, its ID is a number like `1` or `42`.
The `isLocalPath` check only guards against `path_1234567890` style IDs, but the
real issue is that `api.put('/navigation/paths/1/')` expects the path to exist in
the database. If the path was originally created via the localStorage fallback
(due to Bug 1), it has a `path_TIMESTAMP` ID that will never exist in the database.

**Fix:** Change the `updatePath()` logic. Instead of checking the ID format, check
whether the API call **succeeds**. If the API returns a 404 (path not in DB), treat it
as a new path and call `createPath()` instead of silently falling back to localStorage.
This handles the case where a path was previously saved to localStorage only and needs
to be migrated to the database on the next edit.

Updated logic:
```js
async updatePath(id, updates) {
  const currentPath = this.paths.value[id]
  if (!currentPath) throw new Error(`Path with ID ${id} not found`)

  try {
    const apiData = this.toApiFormat({ ...currentPath, ...updates, id })
    const response = await api.put(`/navigation/paths/${id}/`, apiData)
    let updatedPath = this.normalizePath(response.data)
    if ((!updatedPath.visualPoints || updatedPath.visualPoints.length === 0) && updates.visualPoints) {
      updatedPath = { ...updatedPath, visualPoints: updates.visualPoints }
    }
    this.paths.value = { ...this.paths.value, [updatedPath.id]: updatedPath }
    this.saveToStorage()
    return updatedPath
  } catch (error) {
    // If 404, the path only exists in localStorage — migrate it to the DB
    if (error.response?.status === 404) {
      console.warn(`[PathManager] Path ${id} not in DB, migrating via createPath...`)
      const migrated = await this.createPath({ ...currentPath, ...updates })
      // Remove old localStorage-only entry
      const newPaths = { ...this.paths.value }
      delete newPaths[id]
      this.paths.value = { ...newPaths, [migrated.id]: migrated }
      this.saveToStorage()
      return migrated
    }
    throw error  // re-throw real errors so the UI can show them
  }
}
```

---

### Bug 3 — `loadPaths()` merge logic causes localStorage to override the database

**File:** `frontend/src/services/pathManager.js` — `loadPaths()` method

When loading paths, the code merges localStorage data with API data:

```js
if (hasLocalData && pathsArray.length > 0) {
  const mergedPaths = { ...localData }   // localStorage as BASE
  pathsArray.forEach(path => {
    mergedPaths[path.id] = this.normalizePath(path)  // API overwrites where IDs match
  })
  this.paths.value = mergedPaths
  this.saveToStorage()
  return mergedPaths
}
```

The problem: localStorage is used as the **base**, meaning `path_TIMESTAMP` entries
from old localStorage-only saves are always included, even after the database has the
same paths (possibly under different IDs). This causes ghost paths to appear — paths
that exist in localStorage but not in the database — which look correct on the current
device but are invisible everywhere else.

**Fix:** On a successful API response, **always treat the API as the source of truth**.
Do not merge localStorage paths on top of API data. Instead:
1. Load from API
2. Overwrite the in-memory state with API data only
3. Update localStorage to match (so it's a clean cache of the API, not an additive store)

If the API returns an empty array (no paths yet), check localStorage as a one-time
migration source — but clearly log that migration is happening.

Updated `loadPaths()`:
```js
async loadPaths() {
  try {
    const response = await api.get('/navigation/paths/')
    const pathsArray = response.data || []

    // API is source of truth — build paths from API data only
    const pathsObj = {}
    pathsArray.forEach(path => {
      pathsObj[path.id] = this.normalizePath(path)
    })

    // One-time migration: if DB is empty but localStorage has data, offer to migrate
    if (pathsArray.length === 0) {
      const localData = this.loadFromStorage()
      const localPaths = Object.values(localData).filter(p => p.name) // filter valid paths
      if (localPaths.length > 0) {
        console.warn(`[PathManager] DB is empty but localStorage has ${localPaths.length} paths. Migrating...`)
        for (const localPath of localPaths) {
          try {
            await this.createPath(localPath)
          } catch (e) {
            console.error('[PathManager] Migration failed for path:', localPath.name, e)
          }
        }
        // Reload after migration
        const retryResponse = await api.get('/navigation/paths/')
        const retryArray = retryResponse.data || []
        retryArray.forEach(path => {
          pathsObj[path.id] = this.normalizePath(path)
        })
        localStorage.removeItem(STORAGE_KEY)  // clear migrated localStorage data
      }
    }

    this.paths.value = pathsObj
    this.saveToStorage()  // update localStorage cache
    return pathsObj
  } catch (error) {
    console.warn('[PathManager] API failed, using localStorage cache:', error)
    const localData = this.loadFromStorage()
    this.paths.value = localData
    return localData
  }
}
```

---

### Bug 4 — `render.yaml` has no DATABASE_URL — app uses SQLite in production

**File:** `render.yaml`

The root cause of all cross-device data loss is that even if the API calls succeed,
**there is no PostgreSQL database connected in production**. Without `DATABASE_URL`,
Django silently uses SQLite. SQLite on Render's free tier is stored on an ephemeral
filesystem — it is wiped on every redeploy, dyno restart, or sleep cycle.

This means:
- Path created on Device A → saved to Django → saved to SQLite on Render
- Render restarts (after idle timeout or redeploy) → SQLite is wiped
- Device B opens the app → database is empty → API returns `[]`
- localStorage merge logic (Bug 3) kicks in and shows Device B nothing (its
  localStorage is empty), while Device A still sees stale localStorage data

**Fix:** You cannot fix this in code alone — a PostgreSQL database must be provisioned
in Render. Do the following:

1. In `render.yaml`, update the backend service to reference a PostgreSQL database:

```yaml
databases:
  - name: technopath-db
    databaseName: technopath
    user: technopath

services:
  - type: web
    name: technopath-backend
    # ... existing config ...
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: technopath-db
          property: connectionString
      # ... rest of envVars ...
```

2. Add a note in `render.yaml` explaining that after the first deploy with PostgreSQL,
   the admin should run migrations manually via the Render shell:
```
# After first deploy: open Render shell and run:
# python manage.py migrate
# python manage.py seed_default_data (if needed)
```

3. In `backend_django/technopath/settings.py`, confirm the database config uses
   `DATABASE_URL` with a proper fallback:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```
If `dj_database_url` is not in `requirements.txt`, add it.

---

## Summary of Files to Change

| File | Change |
|------|--------|
| `frontend/src/services/pathManager.js` | Fix Bug 1: remove `useApi.value = false` from catch block |
| `frontend/src/services/pathManager.js` | Fix Bug 2: replace `isLocalPath` check with 404-aware migration in `updatePath()` |
| `frontend/src/services/pathManager.js` | Fix Bug 3: rewrite `loadPaths()` to treat API as source of truth with one-time localStorage migration |
| `render.yaml` | Fix Bug 4: add `databases` block and link `DATABASE_URL` via `fromDatabase` |
| `backend_django/technopath/settings.py` | Confirm `dj_database_url` is used for `DATABASES` config |
| `backend_django/requirements.txt` | Add `dj-database-url>=2.0` if not already present |

---

## After All Fixes

1. Deploy to Render and confirm a PostgreSQL database is provisioned and connected.
2. Open the Render shell for the backend service and run:
   ```
   python manage.py migrate
   ```
3. Test cross-device sync:
   - On Device A: create a new path in AdminPathManager and save it.
   - On Device B: open the app and confirm the path appears.
4. Test offline fallback:
   - Disconnect from the network, create a path → it should save to localStorage.
   - Reconnect → on next `loadPaths()`, the API should be tried again.
5. Confirm no paths are being created with `path_TIMESTAMP` IDs in the database
   (all new paths should receive integer IDs from PostgreSQL).
