<template>
  <div class="add-enquiry-view">
    <div class="page-container">
      <!-- AI Paste & Quick Extract Box -->
      <div class="card paste-card">
        <div class="card-header">
          <div class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
            </svg>
          </div>
          <div>
            <h2 class="card-title">1. Paste Raw Customer Message</h2>
            <p class="card-sub">Paste any WhatsApp, Facebook, or Website message (Bangla, Banglish, or English) to auto-extract CRM fields.</p>
          </div>
        </div>

        <div class="paste-form">
          <div class="channel-select-bar">
            <label>Origin Channel:</label>
            <div class="channel-options">
              <label v-for="ch in ['whatsapp', 'facebook', 'website', 'phone']" :key="ch" class="radio-label">
                <input type="radio" v-model="incomingSource" :value="ch" />
                <span class="capitalize">{{ ch }}</span>
              </label>
            </div>
          </div>

          <textarea
            v-model="rawMessage"
            rows="4"
            placeholder="e.g. Assalamualaikum, apnader 3 day bootcamp er price koto? Payment kibhabe korbo?"
            class="raw-textarea"
          ></textarea>

          <div class="paste-actions">
            <button
              type="button"
              :disabled="!rawMessage.trim() || extracting"
              class="btn-extract"
              @click="handleExtract"
            >
              <div v-if="extracting" class="spinner-sm"></div>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
              </svg>
              <span>{{ extracting ? 'Analyzing message with AI...' : 'Extract with AI' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Form Card: Edit & Save -->
      <div class="card form-card">
        <div class="card-header">
          <div class="header-icon green">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </div>
          <div>
            <h2 class="card-title">2. Review & Save Enquiry</h2>
            <p class="card-sub">AI pre-fills the data. You can refine or edit details before saving into the CRM database.</p>
          </div>
        </div>

        <EnquiryForm
          :initial-data="extractedData"
          :saving="saving"
          @save="handleSave"
        />

        <div v-if="saveSuccess" class="success-banner">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <span>Enquiry saved successfully!</span>
          <RouterLink to="/" class="pipeline-link">Go to Pipeline Board &rarr;</RouterLink>
        </div>
      </div>

      <!-- Suggested Reply Box -->
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
    store.showToast('Processed using rule engine.', 'info')
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

.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1.25rem;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon.green {
  background: var(--success-light);
  color: var(--success);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}

.card-sub {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.channel-select-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

.channel-options {
  display: flex;
  gap: 1rem;
}

.radio-label {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  color: var(--text-main);
}

.capitalize {
  text-transform: capitalize;
}

.raw-textarea {
  width: 100%;
  padding: 0.85rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--input-border);
  font-size: 0.925rem;
  color: var(--text-main);
  background-color: var(--input-bg);
  resize: vertical;
}

.raw-textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.paste-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.75rem;
}

.btn-extract {
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #fff;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.875rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
}

.btn-extract:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-sm {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-banner {
  background-color: var(--success-light);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: var(--success);
  padding: 0.85rem 1.25rem;
  border-radius: var(--radius-sm);
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.pipeline-link {
  margin-left: auto;
  color: var(--success);
  text-decoration: underline;
}
</style>
