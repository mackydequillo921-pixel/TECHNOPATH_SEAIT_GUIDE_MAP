import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'
import { shallowRef, h } from 'vue'

// Error boundary component for failed lazy loads
const ErrorComponent = {
  name: 'LoadError',
  setup() {
    return () => h('div', { 
      style: 'padding: 40px; text-align: center; color: #666;' 
    }, [
      h('span', { class: 'material-icons', style: 'font-size: 48px; color: #ccc; display: block; margin-bottom: 16px;' }, 'error_outline'),
      h('p', 'Failed to load page. Please refresh to try again.')
    ])
  }
}

// Helper to handle lazy loading with error boundary
const lazyLoad = (importFn) => {
  return async () => {
    try {
      return await importFn()
    } catch (err) {
      console.error('[Router] Failed to load component:', err)
      return ErrorComponent
    }
  }
}

const routes = [
  // Splash screen
  { path: '/splash', component: lazyLoad(() => import('../views/SplashScreen.vue')) },

  // Public mobile routes
  { path: '/',             component: lazyLoad(() => import('../views/HomeView.vue')) },
  { path: '/map',          component: lazyLoad(() => import('../views/MapView.vue')) },
  { path: '/navigate',     component: lazyLoad(() => import('../views/NavigateView.vue')) },
  { path: '/chatbot',      component: lazyLoad(() => import('../views/ChatbotView.vue')) },
  { path: '/notifications',component: lazyLoad(() => import('../views/NotificationsView.vue')) },
  { path: '/settings',     component: lazyLoad(() => import('../views/SettingsView.vue')) },
  { path: '/profile',      component: lazyLoad(() => import('../views/ProfileView.vue')) },
  { path: '/favorites',    component: lazyLoad(() => import('../views/FavoritesView.vue')) },
  { path: '/feedback',     component: lazyLoad(() => import('../views/FeedbackView.vue')) },


  // Info pages
  { path: '/building-info',   component: lazyLoad(() => import('../views/InfoView.vue')), props: { type: 'buildings' } },
  { path: '/rooms-info',      component: lazyLoad(() => import('../views/InfoView.vue')), props: { type: 'rooms' } },
  { path: '/instructor-info', component: lazyLoad(() => import('../views/InfoView.vue')), props: { type: 'instructors' } },
  { path: '/employees',       component: lazyLoad(() => import('../views/InfoView.vue')), props: { type: 'employees' } },
  { path: '/info/:type',      component: lazyLoad(() => import('../views/InfoView.vue')), props: true },

  // Admin routes
  { path: '/admin/login', component: lazyLoad(() => import('../views/AdminLoginView.vue')) },
  {
    path: '/admin',
    component: lazyLoad(() => import('../views/AdminView.vue')),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  // Show splash only when directly accessing home (initial load/refresh)
  // NOT when navigating from other pages like /navigate, /settings, etc.
  // from.matched.length === 0 means no previous route (initial load)
  const isInitialLoad = from.matched.length === 0
  if (to.path === '/' && isInitialLoad) {
    next('/splash')
    return
  }

  // Handle session expired parameter
  if (to.query.session_expired) {
    // Show toast notification for session expiration
    import('../services/toast.js').then(({ showToast }) => {
      showToast('Your session has expired. Please log in again.', 'warning', 5000)
    })
    // Remove query param after showing toast
    const { session_expired, ...otherQuery } = to.query
    next({ path: to.path, query: otherQuery, replace: true })
    return
  }

  if (to.meta.requiresAuth) {
    const authStore = useAuthStore()
    if (!authStore.isLoggedIn) {
      next('/admin/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
