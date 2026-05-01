# TechnoPath — Admin Notification Badge for Announcements

## What to Build
When an admin or super admin publishes an announcement, a notification badge
(unread count indicator) must appear on the "Send Notification" nav button in
the AdminView sidebar. The backend already has an `UnreadCountView` endpoint at
`GET /api/notifications/unread-count/` — it just needs to be connected to the
frontend sidebar.

---

## Context (Current State)

- The sidebar already shows a badge on "Announcements" (`myPendingCount`) and
  "Pending Approvals" (`pendingCount`) — both work correctly.
- The "Send Notification" nav button has **no badge** at all.
- `AdminView.vue` already has `pendingCount` and `myPendingCount` as `ref(0)`.
- The backend `UnreadCountView` already exists and returns `{ unread_count: N }`.
- When an announcement is published, `Announcement.publish()` automatically creates
  a `Notification` record — so unread count will increase on each new announcement.

---

## Fix 1 — Add `unreadNotifCount` ref and polling in `AdminView.vue`

**File:** `frontend/src/views/AdminView.vue`

### Step 1a — Add the ref

Find where `pendingCount` and `myPendingCount` are declared (around line 216):
```js
const pendingCount   = ref(0)
const myPendingCount = ref(0)
```

Add one new line below them:
```js
const unreadNotifCount = ref(0)
```

### Step 1b — Add the fetch function

Find the `loadPendingCount` function and add a new function right after it:
```js
async function loadUnreadNotifCount() {
  if (!auth.isLoggedIn) return
  try {
    const r = await api.get('/notifications/unread-count/')
    unreadNotifCount.value = r.data.unread_count || 0
  } catch {
    unreadNotifCount.value = 0
  }
}
```

### Step 1c — Call it on mount and poll every 30 seconds

Find the `onMounted` block and add the call + polling interval:
```js
onMounted(() => {
  if (!auth.isLoggedIn) { router.push('/admin/login'); return }
  loadPendingCount()
  loadUnreadNotifCount()   // ← add this

  // Poll every 30 seconds so badge stays in sync
  const notifPoll = setInterval(loadUnreadNotifCount, 30000)

  const routeSection = router.currentRoute.value.query.section
  if (routeSection && [...]) {
    section.value = routeSection
  }

  window.addEventListener('admin-navigate', handleAdminNavigate)

  onUnmounted(() => {
    clearInterval(notifPoll)   // ← add this inside onUnmounted
    window.removeEventListener('admin-navigate', handleAdminNavigate)
  })
})
```

### Step 1d — Reset to 0 when admin navigates to the notifications section

Find the `go(sec)` function or wherever `section.value = sec` is set.
After setting the section, add:
```js
function go(sec) {
  section.value = sec
  if (sec === 'notifications') {
    unreadNotifCount.value = 0   // ← clear badge when user opens the section
  }
}
```

---

## Fix 2 — Show the badge on the "Send Notification" nav button

**File:** `frontend/src/views/AdminView.vue` (template section)

Find the "Send Notification" button in the sidebar (around line 75):
```html
<button v-if="auth.canSendCampusNotification"
        :class="navCls('notifications')" @click="go('notifications')">
  <span class="material-icons tp-nav-icon">notifications_active</span>
  <span>Send Notification</span>
</button>
```

Add the badge span inside it:
```html
<button v-if="auth.canSendCampusNotification"
        :class="navCls('notifications')" @click="go('notifications')">
  <span class="material-icons tp-nav-icon">notifications_active</span>
  <span>Send Notification</span>
  <span v-if="unreadNotifCount > 0" class="tp-nav-badge tp-badge-notif">
    {{ unreadNotifCount > 99 ? '99+' : unreadNotifCount }}
  </span>
</button>
```

---

## Fix 3 — Add badge style

**File:** `frontend/src/views/AdminView.vue` (style section at the bottom)

The existing `.tp-nav-badge` style is already defined. Add one variant for the
notification badge with a distinct color so it's visually different from the
"Pending Approvals" urgent red badge:

```css
.tp-badge-notif {
  background: #1976D2;   /* blue — distinct from red urgent badge */
  color: #fff;
}
```

---

## Fix 4 — Also refresh count after admin sends a notification

**File:** `frontend/src/components/admin/AdminSendNotification.vue`

When the admin successfully sends a notification, emit an event so AdminView
can refresh the count immediately (without waiting for the 30s poll).

Find the success handler after `api.post('/notifications/send/', ...)` succeeds
and add:
```js
// Trigger AdminView to refresh unread count
window.dispatchEvent(new CustomEvent('notification-sent'))
```

Then in `AdminView.vue`, listen for this event in `onMounted`:
```js
window.addEventListener('notification-sent', loadUnreadNotifCount)
```

And remove it in `onUnmounted`:
```js
window.removeEventListener('notification-sent', loadUnreadNotifCount)
```

---

## Summary of Files to Change

| File | Change |
|------|--------|
| `frontend/src/views/AdminView.vue` | Add `unreadNotifCount` ref, `loadUnreadNotifCount()` function, polling interval, badge in template, and `.tp-badge-notif` CSS |
| `frontend/src/components/admin/AdminSendNotification.vue` | Dispatch `notification-sent` event on successful send |

No backend changes needed — `UnreadCountView` at `/api/notifications/unread-count/`
already exists and works correctly.
