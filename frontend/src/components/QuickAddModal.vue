<template>
  <div class="modal-backdrop" @click="handleBackdropClick">
    <div class="modal-dialog quick-add-dialog" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <div class="header-left">
          <div class="header-icon-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
            </svg>
          </div>
          <div>
            <h3 class="modal-title">Quick Add Enquiry</h3>
            <p class="modal-sub">AI auto-extracts fields and drafts reply matching language</p>
          </div>
        </div>

        <button type="button" class="btn-close" @click="$emit('close')">&times;</button>
      </div>

      <!-- Body -->
      <div class="modal-body quick-add-body">
        <!-- Message input step -->
        <div class="quick-step-card">
          <div class="source-select-row">
            <span class="field-label">Channel:</span>
            <div class="channel-chips">
              <label
                v-for="ch in ['whatsapp', 'facebook', 'website', 'phone']"
                :key="ch"
                class="channel-chip-btn"
                :class="{ active: form.source === ch }"
              >
                <input type="radio" v-model="form.source" :value="ch" class="sr-only" />
                <span class="capitalize">{{ ch }}</span>
              </label>
            </div>
          </div>

          <div class="message-input-group">
            <div v-if="analyzing" class="modal-scanner-line"></div>
            <textarea
              v-model="rawMessage"
              rows="3"
              placeholder="Paste enquiry in Bangla, Banglish, or English e.g. 'Bootcamp er details and fees koto? 01711223344'..."
              class="quick-textarea"
            ></textarea>
            <button
              type="button"
              :disabled="!rawMessage.trim() || analyzing"
              class="btn-analyze"
              @click="handleAnalyze"
            >
              <div v-if="analyzing" class="spinner-sm"></div>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
              </svg>
              <span>{{ analyzing ? 'Analyzing with AI...' : 'Auto-fill with AI' }}</span>
            </button>
          </div>
        </div>

        <!-- Form fields -->
        <div class="quick-fields-grid">
          <div class="form-group">
            <label class="field-label">Prospect Name</label>
            <input
              v-model="form.name"
              type="text"
              placeholder="e.g. Tanvir Ahmed"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="field-label">Phone Number</label>
            <input
              v-model="form.phone"
              type="text"
              placeholder="01XXXXXXXXX"
              class="form-input font-mono"
            />
          </div>

          <div class="form-group">
            <label class="field-label">Program Track</label>
            <select v-model="form.interest" class="form-select">
              <option value="bootcamp">Bootcamp (Short / 3-day / Masterclass)</option>
              <option value="fellowship">Fellowship (6-month / Cohort)</option>
              <option value="corporate">Corporate Training (B2B)</option>
              <option value="unknown">General / Unknown</option>
            </select>
          </div>

          <div class="form-group">
            <label class="field-label">Initial Stage</label>
            <select v-model="form.status" class="form-select">
              <option value="New">New</option>
              <option value="Contacted">Contacted</option>
              <option value="Interested">Interested</option>
              <option value="Paid">Paid</option>
              <option value="Lost">Lost</option>
            </select>
          </div>

          <div class="form-group full-col">
            <label class="field-label">Category</label>
            <div class="category-radio-group">
              <label
                v-for="cat in [
                  { val: 'sales', label: 'Sales Lead (Pipeline)' },
                  { val: 'support', label: 'Support Request' },
                  { val: 'job_seeker', label: 'Job Seeker' },
                  { val: 'spam', label: 'Spam' }
                ]"
                :key="cat.val"
                class="category-chip"
                :class="{ active: form.enquiry_type === cat.val }"
              >
                <input type="radio" v-model="form.enquiry_type" :value="cat.val" class="sr-only" />
                <span>{{ cat.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- AI Suggested Reply Preview -->
        <div v-if="suggestedReply || generatingReply" class="reply-preview-card">
          <div class="reply-preview-header">
            <div class="reply-title-group">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <span class="reply-title">AI Suggested Reply</span>
              <span v-if="form.language" class="badge-lang">
                Matches: {{ form.language === 'english' ? 'English' : (form.language === 'bangla' ? 'বাংলা (Bangla)' : 'Banglish') }}
              </span>
            </div>
            <button
              v-if="suggestedReply && !generatingReply"
              type="button"
              class="btn-copy-sm"
              @click="copyReply"
            >
              {{ copied ? 'Copied!' : 'Copy' }}
            </button>
          </div>

          <div v-if="generatingReply" class="reply-skeleton">
            <div class="skeleton-line full skeleton-pulse"></div>
            <div class="skeleton-line md skeleton-pulse"></div>
          </div>
          <p v-else class="reply-preview-text">{{ suggestedReply }}</p>
        </div>
      </div>

      <!-- Footer CTA -->
      <div class="modal-footer">
        <button type="button" class="btn-cancel" @click="$emit('close')">Cancel</button>
        <button
          type="button"
          :disabled="!canSave"
          class="btn-save"
          @click="handleSave"
        >
          <div v-if="saving" class="spinner-sm"></div>
          <span>{{ saving ? 'Saving to CRM...' : 'Save Lead' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import api from '../api/client'

const props = defineProps({
  initialStatus: {
    type: String,
    default: 'New'
  }
})

const emit = defineEmits(['close', 'saved'])
const store = useEnquiriesStore()

const rawMessage = ref('')
const analyzing = ref(false)
const generatingReply = ref(false)
const saving = ref(false)
const suggestedReply = ref('')
const copied = ref(false)

const form = reactive({
  name: '',
  phone: '',
  source: 'whatsapp',
  interest: 'unknown',
  enquiry_type: 'sales',
  status: props.initialStatus || 'New',
  language: 'banglish'
})

const canSave = computed(() => {
  return !saving.value && (
    rawMessage.value.trim().length > 0 ||
    form.name.trim().length > 0 ||
    form.phone.trim().length > 0
  )
})

function handleBackdropClick(e) {
  if (saving.value) return
  if (e.target === e.currentTarget) {
    emit('close')
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && !saving.value) {
    emit('close')
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})

async function handleAnalyze() {
  if (analyzing.value) return
  if (!rawMessage.value.trim()) return
  analyzing.value = true
  generatingReply.value = true

  try {
    const extractRes = await api.extract({
      message: rawMessage.value.trim(),
      source: form.source
    })

    if (extractRes?.data) {
      const data = extractRes.data
      if (data.name) form.name = data.name.trim()
      if (data.phone) form.phone = data.phone.trim()
      if (data.source) form.source = data.source
      if (data.interest) form.interest = data.interest
      if (data.enquiry_type) form.enquiry_type = data.enquiry_type
      if (data.language) form.language = data.language
      store.showToast('Fields auto-filled from message!', 'success')
    } else {
      store.showToast('Message analyzed with rules.', 'info')
    }

    const replyRes = await api.suggestReply({
      message: rawMessage.value.trim(),
      name: form.name,
      interest: form.interest,
      enquiry_type: form.enquiry_type,
      language: form.language
    })

    if (replyRes?.data) {
      suggestedReply.value = replyRes.data.reply
    }
  } catch (err) {
    console.error("AI analysis error:", err)
    store.showToast('Processed using rules.', 'info')
  } finally {
    analyzing.value = false
    generatingReply.value = false
  }
}

function copyReply() {
  if (copied.value || !suggestedReply.value) return
  navigator.clipboard.writeText(suggestedReply.value)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

async function handleSave() {
  if (saving.value) return
  const cleanMsg = rawMessage.value.trim()
  const cleanName = form.name.trim()
  const cleanPhone = form.phone.trim()

  if (!cleanMsg && !cleanName && !cleanPhone) {
    store.showToast('Please enter an enquiry message or prospect name/phone', 'error')
    return
  }

  saving.value = true
  try {
    const payload = {
      name: cleanName || null,
      phone: cleanPhone || null,
      source: form.source,
      interest: form.interest,
      enquiry_type: form.enquiry_type,
      status: form.status,
      language: form.language,
      message: cleanMsg || `Direct enquiry for ${cleanName || cleanPhone || 'Prospect'}`,
      ai_reply: suggestedReply.value ? suggestedReply.value.trim() : null
    }

    await store.addEnquiry(payload)
    emit('saved')
    emit('close')
  } catch (err) {
    store.showToast('Save failed: ' + (err.message || 'Unknown error'), 'error')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--modal-overlay);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-dialog {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg), 0 25px 50px -12px rgba(0, 0, 0, 0.7);
  animation: scaleUp 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
  position: relative;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { transform: scale(0.95) translateY(8px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}

.quick-add-dialog {
  max-width: 640px;
  width: 95%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.15rem 1.4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-surface);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.header-icon-box {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px var(--primary-glow);
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-main);
}

.modal-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.6rem;
  color: var(--text-muted);
  cursor: pointer;
  line-height: 1;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}

.btn-close:hover {
  color: var(--danger);
  background: var(--bg-surface-elevated);
}

.quick-add-body {
  padding: 1.25rem 1.4rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.quick-step-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.source-select-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.channel-chips {
  display: flex;
  gap: 0.35rem;
}

.channel-chip-btn {
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
}

.channel-chip-btn.active {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}

.message-input-group {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.modal-scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--primary) 50%, transparent);
  box-shadow: 0 0 10px var(--primary), 0 0 18px var(--primary);
  z-index: 10;
  animation: modal-scan 1.4s ease-in-out infinite alternate;
  pointer-events: none;
}

@keyframes modal-scan {
  0% { top: 0%; opacity: 0.3; }
  50% { opacity: 1; }
  100% { top: 85%; opacity: 0.3; }
}

.quick-textarea {
  width: 100%;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--input-text);
  font-size: 0.88rem;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
}

.quick-textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-glow);
}

.btn-analyze {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--primary-glow);
  transition: all 0.2s;
}

.btn-analyze:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quick-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}

.full-col {
  grid-column: 1 / -1;
}

.field-label {
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-bottom: 0.35rem;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--input-text);
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-select:focus {
  border-color: var(--primary);
}

.category-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.category-chip {
  padding: 0.35rem 0.7rem;
  border-radius: var(--radius-md);
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.category-chip.active {
  background: rgba(225, 29, 72, 0.15);
  border-color: var(--primary);
  color: var(--primary);
  font-weight: 700;
}

.reply-preview-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.reply-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reply-title-group {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.reply-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-main);
}

.badge-lang {
  font-size: 0.7rem;
  background: var(--bg-surface);
  color: var(--text-muted);
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
}

.btn-copy-sm {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-copy-sm:hover {
  background: var(--primary);
  color: #ffffff;
}

.reply-preview-text {
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--text-main);
  white-space: pre-wrap;
}

.reply-skeleton {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.modal-footer {
  padding: 1rem 1.4rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-surface);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-cancel {
  padding: 0.55rem 1.15rem;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-save {
  padding: 0.55rem 1.35rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--primary-glow);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>

