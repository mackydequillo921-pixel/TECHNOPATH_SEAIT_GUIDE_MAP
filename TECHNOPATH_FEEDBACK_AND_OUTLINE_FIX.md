# TechnoPath — Fix Feedback Submit + Remove Orange Outline

---

## Bug 1 — Feedback "Failed to submit" error

**Root cause:** `frontend/src/services/api.js` has the `baseURL` hardcoded to
`http://localhost:8000/api` instead of reading the environment variable.
This means every API call in production hits localhost (which doesn't exist),
causing the feedback POST to immediately fail.

**File:** `frontend/src/services/api.js`

Find this line:
```js
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
```

Replace with:
```js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
```

That's the only change needed for this file.

---

## Bug 2 — Orange outline box visible on Quick Search tutorial step

The onboarding tutorial shows an orange pulsing border around the search bar.
This is the `.highlight-pulse` element inside `.onboarding-highlight`.
The user wants this highlight removed from the search step only.

**File:** `frontend/src/components/OnboardingTutorial.vue`

Find the `steps` array and the `search` step entry (around line 75):
```js
{
  icon: 'search',
  title: 'Quick Search',
  description: '...',
  highlight: 'search'   // ← change this to null
},
```

Change `highlight: 'search'` to `highlight: null`.

This removes the orange outline box for the Quick Search step only.
All other tutorial step highlights (map, favorites, chatbot, navigate) are unaffected.

---

## Files to change

| File | Change |
|------|--------|
| `frontend/src/services/api.js` | Replace hardcoded `localhost:8000` with `import.meta.env.VITE_API_BASE_URL` |
| `frontend/src/components/OnboardingTutorial.vue` | Set `highlight: null` on the search step |
