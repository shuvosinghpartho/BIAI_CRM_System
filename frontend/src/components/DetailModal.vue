<template>
  <div v-if="enquiry" class="modal-backdrop" @click="handleBackdropClick">
    <div class="modal-dialog" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <div class="header-left">
          <div class="avatar-circle">
            {{ (enquiry.name ? enquiry.name[0] : 'U').toUpperCase() }}
          </div>
          <div>
            <div class="title-row">
              <h3 class="modal-title">{{ enquiry.name || 'Anonymous Prospect' }}</h3>
              <button
                type="button"
                class="btn-edit-toggle"
                :title="isEditing ? 'Cancel Edit' : 'Edit Lead Details'"
                @click="isEditing = !isEditing"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                <span>{{ isEditing ? 'Cancel' : 'Edit' }}</span>
              </button>
            </div>
            <span v-if="enquiry.phone" class="modal-phone font-mono">
              <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
              {{ enquiry.phone }}
            </span>
          </div>
        </div>

        <div class="header-right">
          <OverdueBadge :overdue="isOverdue" />
          <button type="button" class="btn-close" @click="emit('close')">&times;</button>
        </div>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <!-- Quick Action Bar (WhatsApp, Call, Mark Contacted) -->
        <div class="quick-action-bar">
          <a
            v-if="cleanPhone"
            :href="`https://wa.me/88${cleanPhone}`"
            target="_blank"
            rel="noopener noreferrer"
            class="action-btn wa-btn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
            </svg>
            <span>WhatsApp Lead</span>
          </a>

          <a
            v-if="cleanPhone"
            :href="`tel:${cleanPhone}`"
            class="action-btn call-btn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
            </svg>
            <span>Call Lead</span>
          </a>

          <button
            v-if="isOverdue || enquiry.status === 'New'"
            type="button"
            class="action-btn contact-btn"
            @click="markAsContacted"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Mark Contacted</span>
          </button>
        </div>

        <!-- Inline Edit Section -->
        <div v-if="isEditing" class="edit-fields-card">
          <div class="edit-fields-grid">
            <div class="edit-field">
              <label class="section-label">Prospect Name</label>
              <input v-model="editForm.name" type="text" class="edit-input" />
            </div>

            <div class="edit-field">
              <label class="section-label">Phone Number</label>
              <input v-model="editForm.phone" type="text" class="edit-input font-mono" />
            </div>

            <div class="edit-field">
              <label class="section-label">Program Track</label>
              <select v-model="editForm.interest" class="edit-input">
                <option value="bootcamp">Bootcamp</option>
                <option value="fellowship">Fellowship</option>
                <option value="corporate">Corporate Training</option>
                <option value="unknown">Unknown</option>
              </select>
            </div>

            <div class="edit-field">
              <label class="section-label">Channel Source</label>
              <select v-model="editForm.source" class="edit-input">
                <option value="whatsapp">WhatsApp</option>
                <option value="facebook">Facebook</option>
                <option value="website">Website</option>
                <option value="phone">Phone</option>
              </select>
            </div>
          </div>
          <div class="edit-actions">
            <button type="button" class="btn-save-inline" @click="saveEdits">
              Save Lead Details
            </button>
          </div>
        </div>

        <!-- Status Switcher Bar -->
        <div class="meta-section">
          <label class="section-label">Pipeline Stage:</label>
          <div class="stage-pills">
            <button
              v-for="s in ['New', 'Contacted', 'Interested', 'Paid', 'Lost']"
              :key="s"
              type="button"
              class="stage-btn"
              :class="{ active: enquiry.status === s, [s.toLowerCase()]: true }"
              @click="changeStatus(s)"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <!-- Tag row -->
        <div class="tags-bar">
          <span class="badge" :class="getChannelBadgeClass(enquiry.source)">
            Channel: {{ enquiry.source }}
          </span>
          <span class="badge" :class="getInterestBadgeClass(enquiry.interest)">
            Track: {{ enquiry.interest }}
          </span>
          <span v-if="enquiry.language" class="badge badge-unknown">
            Language: {{ enquiry.language }}
          </span>
          <span v-if="enquiry.enquiry_type" class="badge badge-type">
            Type: {{ enquiry.enquiry_type }}
          </span>
        </div>

        <!-- Full Original Message -->
        <div class="message-card">
          <div class="message-header">
            <span class="section-label">Original Message:</span>
            <span class="timestamp-label">Received {{ formatDate(enquiry.created_at) }}</span>
          </div>
          <p class="message-text">{{ enquiry.message }}</p>
        </div>

        <!-- AI Suggested Reply in modal -->
        <div class="reply-wrapper">
          <ReplyBox
            :reply-text="replyText"
            :language="enquiry.language"
            :loading="generatingReply"
            @update:reply-text="replyText = $event"
          />
          <div class="reply-footer-actions">
            <button
              type="button"
              class="btn-regenerate"
              :disabled="generatingReply"
              @click="regenerateReply"
            >
              <div v-if="generatingReply" class="spinner-sm"></div>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/>
              </svg>
              <span>{{ generatingReply ? 'Generating AI Reply...' : 'Regenerate AI Reply' }}</span>
            </button>
          </div>
        </div>

        <!-- Action / Timeline Footer -->
        <div class="timeline-row">
          <div class="timeline-meta">
            <span>Last Contacted: <strong>{{ enquiry.last_contacted_at ? formatDate(enquiry.last_contacted_at) : 'Never' }}</strong></span>
          </div>
          <button type="button" class="btn-delete" @click="confirmDelete">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
            Delete Lead
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import OverdueBadge from './OverdueBadge.vue'
import ReplyBox from './ReplyBox.vue'
import api from '../api/client'
import { formatDate, getChannelBadgeClass, getInterestBadgeClass } from '../utils/format'

const props = defineProps({
  enquiry: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])
const store = useEnquiriesStore()

const replyText = ref(props.enquiry?.ai_reply || '')
const generatingReply = ref(false)
const isEditing = ref(false)

const editForm = reactive({
  name: props.enquiry?.name || '',
  phone: props.enquiry?.phone || '',
  interest: props.enquiry?.interest || 'unknown',
  source: props.enquiry?.source || 'website'
})

watch(() => props.enquiry, (newVal) => {
  if (newVal) {
    editForm.name = newVal.name || ''
    editForm.phone = newVal.phone || ''
    editForm.interest = newVal.interest || 'unknown'
    editForm.source = newVal.source || 'website'
    if (newVal.ai_reply) {
      replyText.value = newVal.ai_reply
    }
  }
})

const isOverdue = computed(() => props.enquiry ? store.isOverdue(props.enquiry) : false)

const cleanPhone = computed(() => {
  if (!props.enquiry?.phone) return ''
  return props.enquiry.phone.replace(/\D/g, '')
})

async function changeStatus(newStatus) {
  if (props.enquiry) {
    await store.updateStatus(props.enquiry.id, newStatus)
  }
}

async function markAsContacted() {
  if (props.enquiry) {
    await store.updateStatus(props.enquiry.id, 'Contacted')
    store.showToast('Marked as contacted! Overdue alert resolved.', 'success')
  }
}

async function saveEdits() {
  if (!props.enquiry) return
  try {
    const res = await api.updateEnquiry(props.enquiry.id, {
      name: editForm.name.trim() || null,
      phone: editForm.phone.trim() || null,
      interest: editForm.interest,
      source: editForm.source
    })
    const idx = store.enquiries.findIndex(e => e.id === props.enquiry.id)
    if (idx !== -1) {
      store.enquiries[idx] = res.data
    }
    store.activeModalEnquiry = res.data
    isEditing.value = false
    store.showToast('Lead details updated successfully!', 'success')
  } catch (err) {
    store.showToast('Failed to update lead: ' + err.message, 'error')
  }
}

async function regenerateReply() {
  if (!props.enquiry) return
  generatingReply.value = true
  try {
    const res = await api.suggestReply({
      message: props.enquiry.message,
      name: props.enquiry.name,
      interest: props.enquiry.interest,
      enquiry_type: props.enquiry.enquiry_type,
      language: props.enquiry.language
    })
    replyText.value = res.data.reply
    // Persist reply to DB
    await api.updateEnquiry(props.enquiry.id, { ai_reply: replyText.value })
    store.showToast('AI reply regenerated and saved!', 'success')
  } catch (err) {
    console.error(err)
    store.showToast('Failed to generate reply.', 'error')
  } finally {
    generatingReply.value = false
  }
}

function handleBackdropClick(e) {
  if (e.target === e.currentTarget) {
    emit('close')
  }
}

async function confirmDelete() {
  if (confirm("Are you sure you want to delete this enquiry from the CRM?")) {
    await store.deleteEnquiry(props.enquiry.id)
    emit('close')
  }
}

onMounted(async () => {
  if (props.enquiry && !replyText.value) {
    regenerateReply()
  }
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: var(--modal-overlay);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  animation: fadeIn 0.15s ease-out;
}

.modal-dialog {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  width: 95%;
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  animation: scaleUp 0.2s ease-out;
}

@keyframes scaleUp {
  from { transform: scale(0.96); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.avatar-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.15rem;
  flex-shrink: 0;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-main);
}

.btn-edit-toggle {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-edit-toggle:hover {
  color: var(--primary);
  border-color: var(--primary);
}

.modal-phone {
  font-size: 0.825rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.15rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted);
  line-height: 1;
  cursor: pointer;
}

.btn-close:hover {
  color: var(--danger);
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Quick Action Bar */
.quick-action-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-md);
  font-size: 0.8rem;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.wa-btn {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border-color: rgba(16, 185, 129, 0.3);
}
.wa-btn:hover {
  background: #10b981;
  color: #ffffff;
}

.call-btn {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}
.call-btn:hover {
  background: #3b82f6;
  color: #ffffff;
}

.contact-btn {
  background: rgba(225, 29, 72, 0.15);
  color: var(--primary);
  border-color: rgba(225, 29, 72, 0.3);
}
.contact-btn:hover {
  background: var(--primary);
  color: #ffffff;
}

/* Edit fields */
.edit-fields-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.edit-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.edit-input {
  width: 100%;
  padding: 0.45rem 0.65rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  background: var(--input-bg);
  color: var(--input-text);
  font-size: 0.85rem;
  outline: none;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-save-inline {
  padding: 0.4rem 0.9rem;
  background: var(--primary);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
}

.meta-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-label {
  font-size: 0.78rem;
  font-weight: 800;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stage-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.stage-btn {
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.825rem;
  font-weight: 700;
  background: var(--bg-surface-elevated);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  transition: all 0.15s;
  cursor: pointer;
}

.stage-btn.active.new { background: #3b82f6; color: #fff; border-color: #3b82f6; }
.stage-btn.active.contacted { background: #f59e0b; color: #fff; border-color: #f59e0b; }
.stage-btn.active.interested { background: #8b5cf6; color: #fff; border-color: #8b5cf6; }
.stage-btn.active.paid { background: #10b981; color: #fff; border-color: #10b981; }
.stage-btn.active.lost { background: #64748b; color: #fff; border-color: #64748b; }

.tags-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge-type {
  background: rgba(148, 163, 184, 0.15);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.message-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem 1.15rem;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.timestamp-label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.message-text {
  font-size: 0.925rem;
  color: var(--text-main);
  line-height: 1.6;
}

.reply-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.reply-footer-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-regenerate {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-md);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-regenerate:hover:not(:disabled) {
  color: var(--primary);
  border-color: var(--primary);
}

.timeline-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color);
  font-size: 0.825rem;
  color: var(--text-muted);
}

.btn-delete {
  background: none;
  border: none;
  color: var(--danger);
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.btn-delete:hover {
  background: var(--danger-bg);
}
</style>
