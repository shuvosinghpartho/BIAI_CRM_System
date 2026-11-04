<template>
  <div class="add-enquiry-view">
    <div class="page-container">
      <!-- Step 1 Card: AI Message Extraction -->
      <div class="card-box">
        <div class="card-box-header">
          <div class="header-icon-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
            </svg>
          </div>
          <div>
            <h2 class="card-box-title">1. Paste Customer Message</h2>
            <p class="card-box-sub">Paste incoming messages from WhatsApp, Facebook, or Website in Bangla, Banglish, or English.</p>
          </div>
        </div>

        <div class="paste-form">
          <div class="channel-select-bar">
            <span class="bar-label">Source Channel:</span>
            <div class="channel-chips">
              <label
                v-for="ch in ['whatsapp', 'facebook', 'website', 'phone']"
                :key="ch"
                class="chip-label"
                :class="{ selected: incomingSource === ch }"
              >
                <input type="radio" v-model="incomingSource" :value="ch" />
                <span class="capitalize">{{ ch }}</span>
              </label>
            </div>
          </div>

          <textarea
            v-model="rawMessage"
            rows="4"
            placeholder="Paste message here e.g. 'Assalamualaikum, apnader 3 day bootcamp er price koto? Payment kibhabe korbo?'"
            class="raw-textarea"
          ></textarea>

          <div class="paste-actions">
            <button
              type="button"
              :disabled="!rawMessage.trim() || extracting"
              class="btn-primary"
              @click="handleExtract"
            >
              <div v-if="extracting" class="spinner-sm"></div>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
              </svg>
              <span>{{ extracting ? 'Analyzing message with AI...' : 'Analyze with AI' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Step 2 Card: Review & Save Enquiry Form -->
      <div class="card-box">
        <div class="card-box-header">
          <div class="header-icon-box green">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </div>
          <div>
            <h2 class="card-box-title">2. Review & Save Lead Details</h2>
            <p class="card-box-sub">Extracted fields are pre-filled below. Review or edit before saving to the CRM.</p>
          </div>
        </div>

        <EnquiryForm
          :initial-data="extractedData"
          :saving="saving"
          @save="handleSave"
        />

        <div v-if="saveSuccess" class="success-banner">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <span>Enquiry saved to CRM successfully!</span>
          <RouterLink to="/" class="pipeline-link">Go to Sales Pipeline &rarr;</RouterLink>
        </div>
      </div>

      <!-- Step 3 Card: AI Suggested Response Box -->
      <ReplyBox
        :reply-text="suggestedReply"
        :loading="generatingReply"
        :language="extractedData.language"
        @update:reply-text="suggestedReply = $event"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useEnquiriesStore } from '../stores/enquiries'
import EnquiryForm from '../components/EnquiryForm.vue'
import ReplyBox from '../components/ReplyBox.vue'
import api from '../api/client'

const router = useRouter()
const store = useEnquiriesStore()

const incomingSource = ref('whatsapp')
const rawMessage = ref('')
const extracting = ref(false)
const saving = ref(false)
const saveSuccess = ref(false)
const generatingReply = ref(false)
const suggestedReply = ref('')

const extractedData = ref({
  name: '',
  phone: '',
  source: 'whatsapp',
  interest: 'unknown',
  enquiry_type: 'sales',
  language: 'banglish',
  message: ''
})

async function handleExtract() {
  if (!rawMessage.value.trim()) return
  extracting.value = true
  saveSuccess.value = false

  try {
    const res = await api.extract({
      message: rawMessage.value,
      source: incomingSource.value
    })

    extractedData.value = {
      name: res.data.name || '',
      phone: res.data.phone || '',
      source: res.data.source || incomingSource.value,
      interest: res.data.interest || 'unknown',
      enquiry_type: res.data.enquiry_type || 'sales',
      language: res.data.language || 'banglish',
      message: rawMessage.value
    }

    store.showToast('Fields extracted from message!', 'success')
    generateReply()
  } catch (err) {
    console.error("Extraction error:", err)
    extractedData.value.message = rawMessage.value
    extractedData.value.source = incomingSource.value
    store.showToast('Processed using rules.', 'info')
  } finally {
    extracting.value = false
  }
}

async function generateReply() {
  generatingReply.value = true
  try {
    const res = await api.suggestReply({
      message: extractedData.value.message,
      name: extractedData.value.name,
      interest: extractedData.value.interest,
      enquiry_type: extractedData.value.enquiry_type,
      language: extractedData.value.language
    })
    suggestedReply.value = res.data.reply
  } catch (err) {
    console.error("Reply generation error:", err)
  } finally {
    generatingReply.value = false
  }
}

async function handleSave(formData) {
  saving.value = true
  try {
    const payload = {
      ...formData,
      ai_reply: suggestedReply.value || null
    }
    await store.addEnquiry(payload)
    saveSuccess.value = true
    rawMessage.value = ''
  } catch (err) {
    store.showToast("Error saving enquiry: " + err.message, 'error')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.add-enquiry-view {
  padding: 1.5rem 1.75rem;
}

.page-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card-box-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1.25rem;
}

.header-icon-box {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon-box.green {
  background: var(--success-bg);
  color: var(--success);
}

.card-box-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-main);
}

.card-box-sub {
  font-size: 0.825rem;
  color: var(--text-muted);
}

.channel-select-bar {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 0.85rem;
}

.bar-label {
  font-size: 0.825rem;
  font-weight: 700;
  color: var(--text-muted);
}

.channel-chips {
  display: flex;
  gap: 0.5rem;
}

.chip-label {
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  background: var(--bg-surface-elevated);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.15s ease;
}

.chip-label input {
  display: none;
}

.chip-label.selected {
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  border-color: var(--primary);
  box-shadow: 0 2px 8px var(--primary-glow);
}

.capitalize {
  text-transform: capitalize;
}

.raw-textarea {
  width: 100%;
  padding: 0.95rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  font-size: 0.925rem;
  color: var(--input-text);
  background-color: var(--input-bg);
  resize: vertical;
  line-height: 1.5;
}

.raw-textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-glow);
}

.paste-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.85rem;
}

.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-banner {
  background-color: var(--success-bg);
  border: 1px solid rgba(34, 197, 94, 0.4);
  color: var(--success);
  padding: 0.85rem 1.25rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 700;
}

.pipeline-link {
  margin-left: auto;
  color: var(--success);
  text-decoration: underline;
}
</style>
