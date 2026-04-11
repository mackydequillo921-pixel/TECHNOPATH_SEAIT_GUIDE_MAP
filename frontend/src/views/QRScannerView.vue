<template>
  <div class="qrscanner-view">
    <header class="qrscanner-top-bar">
      <button class="qrscanner-back-btn" @click="goBack">
        <span class="material-icons">arrow_back</span>
      </button>
      <h1>QR Scanner</h1>
      <div class="qrscanner-spacer"></div>
    </header>

    <div class="qrscanner-scanner-container">
      <!-- No camera permission -->
      <div v-if="!hasCamera" class="qrscanner-no-camera">
        <span class="material-icons qrscanner-no-camera-icon">photo_camera</span>
        <p>Camera access required</p>
        <p class="qrscanner-subtitle">Please allow camera access to scan QR codes</p>
        <button class="qrscanner-retry-btn" @click="startCamera">
          <span class="material-icons">refresh</span>
          Try Again
        </button>
      </div>

      <!-- Scanning -->
      <div v-else-if="isScanning" class="qrscanner-scanning-area">
        <video ref="videoRef" class="qrscanner-camera-feed" autoplay playsinline muted></video>
        <canvas ref="canvasRef" class="qrscanner-hidden-canvas"></canvas>

        <div class="qrscanner-scan-overlay">
          <div class="qrscanner-scan-frame">
            <div class="qrscanner-corner qrscanner-top-left"></div>
            <div class="qrscanner-corner qrscanner-top-right"></div>
            <div class="qrscanner-corner qrscanner-bottom-left"></div>
            <div class="qrscanner-corner qrscanner-bottom-right"></div>
            <div class="qrscanner-scan-line"></div>
          </div>
          <p class="qrscanner-scan-text">Point camera at QR code</p>
        </div>
      </div>

      <!-- Result -->
      <div v-else-if="scanResult" class="qrscanner-result-panel">
        <div class="qrscanner-result-icon">
          <span class="material-icons">check_circle</span>
        </div>
        <h3>QR Code Detected!</h3>
        <p class="qrscanner-result-data">{{ scanResult }}</p>
        <div class="qrscanner-result-actions">
          <button class="qrscanner-action-btn qrscanner-secondary" @click="resetScan">
            Scan Again
          </button>
          <button class="qrscanner-action-btn qrscanner-primary" @click="processResult">
            Navigate
          </button>
        </div>
      </div>
    </div>

    <!-- Manual entry fallback -->
    <div class="qrscanner-manual-entry">
      <p class="qrscanner-divider-text">— or enter a location code —</p>
      <div class="qrscanner-input-group">
        <input
          v-model="manualCode"
          type="text"
          placeholder="e.g. MST-CL1, RST-REG, LIB"
          @keyup.enter="processManualCode"
        />
        <button @click="processManualCode" :disabled="!manualCode.trim()">Go</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import jsQR from 'jsqr'

const router    = useRouter()
const videoRef  = ref(null)
const canvasRef = ref(null)
const hasCamera  = ref(false)
const isScanning = ref(false)
const scanResult = ref('')
const manualCode = ref('')

let stream       = null
let scanInterval = null

const goBack = () => router.back()

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' },
    })
    if (videoRef.value) {
      videoRef.value.srcObject = stream
      hasCamera.value  = true
      isScanning.value = true
      startScanning()
    }
  } catch {
    hasCamera.value = false
  }
}

function startScanning() {
  scanInterval = setInterval(() => {
    if (!videoRef.value || !canvasRef.value) return
    const video  = videoRef.value
    const canvas = canvasRef.value
    const ctx    = canvas.getContext('2d')

    if (!video.videoWidth) return   // not ready yet

    canvas.width  = video.videoWidth
    canvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    const code = jsQR(imageData.data, imageData.width, imageData.height)

    if (code) {
      scanResult.value = code.data
      isScanning.value = false
      stopCamera()
    }
  }, 200)
}

function stopCamera() {
  if (scanInterval) { clearInterval(scanInterval); scanInterval = null }
  if (stream)       { stream.getTracks().forEach(t => t.stop()); stream = null }
}

function resetScan() {
  scanResult.value = ''
  isScanning.value = true
  startCamera()
}

// FIX: Use query param 'to' — matches what NavigateView reads (was 'destination' before)
function processResult() {
  navigateToLocation(scanResult.value.trim())
}

function processManualCode() {
  if (!manualCode.value.trim()) return
  navigateToLocation(manualCode.value.trim())
}

function navigateToLocation(raw) {
  // Support SEAIT: prefixed QR codes
  const code = raw.startsWith('SEAIT:') ? raw.replace('SEAIT:', '') : raw

  // Map common short codes to full location names
  const codeMap = {
    'MST-CL1': 'CL1', 'MST-CL2': 'CL2', 'MST-CL5': 'CL5', 'MST-CL6': 'CL6',
    'RST-REG': 'Registrar Office', 'RST-ACC': 'Accounting Office',
    'LIB':     'Library', 'CAF': 'Cafeteria', 'GYM': 'Gymnasium',
    'GATE':    'Main Gate',
  }

  const destination = codeMap[code.toUpperCase()] || code

  // FIX: Use 'to' query param (was 'destination' — NavigateView reads 'to')
  router.push({ path: '/navigate', query: { to: destination } })
}

onMounted(startCamera)
onUnmounted(stopCamera)
</script>

<style>
/* ── QR Scanner styles ─────────────────────────────────────── */
.qrscanner-view {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  background: var(--color-bg);
  overflow: hidden;
}

.qrscanner-top-bar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  height: var(--top-bar-height);
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.qrscanner-back-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-full);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
}

.qrscanner-top-bar h1 {
  font-size: var(--text-lg);
  font-weight: 600;
  flex: 1;
}

.qrscanner-spacer { width: 40px; }

.qrscanner-scanner-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #000;
}

.qrscanner-no-camera {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--space-3);
  background: var(--color-surface);
  padding: var(--space-8);
  text-align: center;
}

.qrscanner-no-camera-icon {
  font-size: 64px;
  color: var(--color-primary);
}

.qrscanner-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.qrscanner-retry-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  font-weight: 500;
  margin-top: var(--space-3);
}

.qrscanner-scanning-area {
  position: relative;
  width: 100%;
  height: 100%;
}

.qrscanner-camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.qrscanner-hidden-canvas { display: none; }

.qrscanner-scan-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-5);
}

.qrscanner-scan-frame {
  width: 220px;
  height: 220px;
  position: relative;
}

.qrscanner-corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border-color: var(--color-primary);
  border-style: solid;
}

.qrscanner-top-left     { top: 0; left: 0;  border-width: 3px 0 0 3px; }
.qrscanner-top-right    { top: 0; right: 0; border-width: 3px 3px 0 0; }
.qrscanner-bottom-left  { bottom: 0; left: 0;  border-width: 0 0 3px 3px; }
.qrscanner-bottom-right { bottom: 0; right: 0; border-width: 0 3px 3px 0; }

.qrscanner-scan-line {
  position: absolute;
  left: 0; right: 0;
  height: 2px;
  background: var(--color-primary);
  animation: scanMove 2s ease-in-out infinite;
}

@keyframes scanMove {
  0%, 100% { top: 0; }
  50%       { top: calc(100% - 2px); }
}

.qrscanner-scan-text {
  color: rgba(255,255,255,.85);
  font-size: var(--text-sm);
  font-weight: 500;
  text-align: center;
}

.qrscanner-result-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--space-4);
  background: var(--color-surface);
  padding: var(--space-8);
  text-align: center;
}

.qrscanner-result-icon .material-icons {
  font-size: 56px;
  color: var(--color-success);
}

.qrscanner-result-data {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  background: var(--color-surface-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  word-break: break-all;
  max-width: 100%;
}

.qrscanner-result-actions {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-3);
}

.qrscanner-action-btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-full);
  font-weight: 500;
  cursor: pointer;
  border: none;
  font-size: var(--text-base);
}

.qrscanner-primary {
  background: var(--color-primary);
  color: #fff;
}

.qrscanner-secondary {
  background: var(--color-surface-2);
  color: var(--color-text-primary);
}

.qrscanner-manual-entry {
  padding: var(--space-5) var(--space-4);
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
}

.qrscanner-divider-text {
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-text-hint);
  margin-bottom: var(--space-3);
}

.qrscanner-input-group {
  display: flex;
  gap: var(--space-2);
}

.qrscanner-input-group input {
  flex: 1;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.qrscanner-input-group button {
  padding: var(--space-3) var(--space-5);
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
}

.qrscanner-input-group button:disabled {
  opacity: .5;
  cursor: not-allowed;
}
</style>
