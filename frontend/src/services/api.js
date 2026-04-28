import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

let isRefreshing = false
let refreshSubscribers = []

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('tp_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiry — auto-refresh then retry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    
    // If error is not 401 or already retried, reject immediately
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error)
    }
    
    original._retry = true
    
    // If already refreshing, wait for it
    if (isRefreshing) {
      return new Promise((resolve) => {
        refreshSubscribers.push((token) => {
          original.headers.Authorization = `Bearer ${token}`
          resolve(api(original))
        })
      })
    }
    
    isRefreshing = true
    
    try {
      const refresh = localStorage.getItem('tp_refresh')
      if (!refresh) {
        throw new Error('No refresh token')
      }
      
      const res = await api.post('/auth/refresh/', { refresh })
      const newToken = res.data.access
      localStorage.setItem('tp_token', newToken)
      
      // Notify subscribers
      refreshSubscribers.forEach((callback) => callback(newToken))
      refreshSubscribers = []
      
      original.headers.Authorization = `Bearer ${newToken}`
      return api(original)
    } catch (refreshError) {
      // Token refresh failed - clear auth state and reject properly
      localStorage.removeItem('tp_token')
      localStorage.removeItem('tp_refresh')
      localStorage.removeItem('tp_user')
      
      // Redirect to login if this was an auth-required request
      const authRequired = original.headers.Authorization !== undefined
      if (authRequired && !window.location.pathname.includes('/login')) {
        window.location.href = '/?session_expired=1'
      }
      
      // Reject with a clear error that components can handle
      return Promise.reject({
        ...refreshError,
        isAuthError: true,
        message: 'Session expired. Please log in again.'
      })
    } finally {
      isRefreshing = false
      refreshSubscribers = []
    }
  }
)

export default api
