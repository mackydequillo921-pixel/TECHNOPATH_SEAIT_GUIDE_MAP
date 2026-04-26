<template>
  <div v-if="show" class="offline-banner" :class="{ 'offline': !isOnline, 'stale': isOnline && isStale }">
    <div class="offline-icon-wrap">
      <span class="material-icons offline-icon">
        {{ !isOnline ? 'wifi_off' : 'update' }}
      </span>
      <span v-if="!isOnline" class="offline-pulse"></span>
    </div>
    <div class="offline-content">
      <span class="offline-title">{{ !isOnline ? 'Offline Mode' : 'Cached Data' }}</span>
      <span class="offline-text">{{ message }}</span>
    </div>
    <button v-if="!isOnline" class="offline-dismiss" @click="dismiss" title="Dismiss">
      <span class="material-icons">close</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { isOnline, registerConnectivityListener } from '../services/sync.js'
import { getOfflineStatus } from '../services/offlineData.js'

const show = ref(true)
const onlineStatus = ref(isOnline())
const statusDetails = ref(null)
let unsubscribe = null

const isStale = computed(() => statusDetails.value?.stale || false)

const message = computed(() => {
  if (!onlineStatus.value) {
    if (statusDetails.value?.lastSync) {
      const time = new Date(statusDetails.value.lastSync).toLocaleTimeString()
      return `Offline mode • Last synced at ${time}`
    }
    return 'Offline mode • Using cached data'
  }
  if (isStale.value) {
    return 'Using cached data • Will sync when available'
  }
  return ''
})

async function updateStatus() {
  onlineStatus.value = isOnline()
  if (!onlineStatus.value || show.value) {
    statusDetails.value = await getOfflineStatus()
  }
  // Auto-hide if online and not stale
  if (onlineStatus.value && !isStale.value) {
    show.value = false
  }
}

function dismiss() {
  show.value = false
}

onMounted(() => {
  updateStatus()
  // Listen for connectivity changes
  window.addEventListener('online', updateStatus)
  window.addEventListener('offline', () => {
    onlineStatus.value = false
    show.value = true
  })
  // Register for sync events
  unsubscribe = registerConnectivityListener((result) => {
    if (result.success) {
      updateStatus()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('online', updateStatus)
  window.removeEventListener('offline', updateStatus)
  if (unsubscribe) unsubscribe()
})
</script>

<style scoped>
.offline-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 44px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(8px);
}

.offline-banner.offline {
  background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
  color: white;
}

.offline-banner.stale {
  background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
  color: white;
}

.offline-banner:not(.offline):not(.stale) {
  display: none;
}

.offline-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
}

.offline-icon {
  font-size: 20px;
  z-index: 2;
}

.offline-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  animation: pulse-ring 2s ease-out infinite;
  z-index: 1;
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.offline-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 2px;
}

.offline-title {
  font-weight: 600;
  font-size: 13px;
  line-height: 1.2;
}

.offline-text {
  font-size: 12px;
  opacity: 0.9;
  line-height: 1.2;
}

.offline-dismiss {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.9;
  transition: all 0.2s ease;
  border-radius: 50%;
  width: 32px;
  height: 32px;
}

.offline-dismiss:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.offline-dismiss:active {
  transform: scale(0.95);
}

.offline-dismiss .material-icons {
  font-size: 18px;
}

/* Adjust for safe areas on mobile */
@supports (padding-top: env(safe-area-inset-top)) {
  .offline-banner {
    padding-top: calc(10px + env(safe-area-inset-top));
    min-height: calc(44px + env(safe-area-inset-top));
  }
}

/* Slide in animation */
@keyframes slideInDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.offline-banner {
  animation: slideInDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
