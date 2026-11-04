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
            <h3 class="modal-title">{{ enquiry.name || 'Anonymous Prospect' }}</h3>
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
        <ReplyBox
          :reply-text="replyText"
          :language="enquiry.language"
          :loading="generatingReply"
          @update:reply-text="replyText = $event"
        />

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
import { ref, computed, onMounted } from 'vue'
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

const isOverdue = computed(() => props.enquiry ? store.isOverdue(props.enquiry) : false)

async function changeStatus(newStatus) {
  if (props.enquiry) {
    await store.updateStatus(props.enquiry.id, newStatus)
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
    } catch (err) {
      console.error(err)
    } finally {
      generatingReply.value = false
    }
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
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
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
  font-size: 1.5rem;
  color: var(--text-muted);
  line-height: 1;
}

.btn-close:hover {
  color: var(--text-main);
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.meta-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-label {
  font-size: 0.8rem;
  font-weight: 700;
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
  font-weight: 600;
  background: var(--bg-surface-elevated);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  transition: all 0.15s;
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
  color: var(--danger);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
}

.btn-delete:hover {
  background: var(--danger-light);
}
</style>
