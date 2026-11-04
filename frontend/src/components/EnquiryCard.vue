<template>
  <div class="enquiry-card" :class="{ 'is-overdue': overdue }">
    <div class="card-top">
      <div class="sender-info">
        <h4 class="sender-name">{{ enquiry.name || 'Anonymous Sender' }}</h4>
        <span v-if="enquiry.phone" class="sender-phone">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
          </svg>
          {{ enquiry.phone }}
        </span>
      </div>
      <OverdueBadge :overdue="overdue" />
    </div>

    <!-- Tags Row -->
    <div class="badges-row">
      <span class="badge" :class="getChannelBadgeClass(enquiry.source)">
        {{ enquiry.source }}
      </span>
      <span class="badge" :class="getInterestBadgeClass(enquiry.interest)">
        {{ enquiry.interest }}
      </span>
      <span v-if="enquiry.language" class="badge badge-unknown">
        {{ enquiry.language }}
      </span>
    </div>

    <!-- Message Body -->
    <p class="message-preview" :title="enquiry.message">
      {{ enquiry.message }}
    </p>

    <!-- Footer with Timestamp & Status Dropdown -->
    <div class="card-footer">
      <div class="time-meta">
        <span class="time-text">{{ formatTimeAgo(enquiry.created_at) }}</span>
      </div>
      <StatusSelect
        :model-value="enquiry.status"
        @change="handleStatusChange"
      />
    </div>

    <!-- View / Generate Reply Modal trigger or toggle -->
    <div v-if="showQuickReply" class="quick-reply-section">
      <ReplyBox
        :reply-text="replyText"
        :loading="generatingReply"
        :language="enquiry.language"
        @update:reply-text="replyText = $event"
      />
    </div>

    <div class="card-actions">
      <button
        type="button"
        class="btn-text-action"
        @click="toggleReply"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/>
        </svg>
        {{ showQuickReply ? 'Hide Reply' : 'Suggested Reply' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import StatusSelect from './StatusSelect.vue'
import OverdueBadge from './OverdueBadge.vue'
import ReplyBox from './ReplyBox.vue'
import api from '../api/client'
import {
  formatTimeAgo,
  getChannelBadgeClass,
  getInterestBadgeClass
} from '../utils/format'

const props = defineProps({
  enquiry: {
    type: Object,
    required: true
  }
})

const store = useEnquiriesStore()
const showQuickReply = ref(false)
const generatingReply = ref(false)
const replyText = ref(props.enquiry.ai_reply || '')

const overdue = computed(() => store.isOverdue(props.enquiry))

async function handleStatusChange(newStatus) {
  await store.updateStatus(props.enquiry.id, newStatus)
}

async function toggleReply() {
  showQuickReply.value = !showQuickReply.value
  if (showQuickReply.value && !replyText.value) {
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
    } catch (e) {
      replyText.value = "Failed to generate reply. Please try again."
    } finally {
      generatingReply.value = false
    }
  }
}
</script>

<style scoped>
.enquiry-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  transition: all 0.15s ease;
}

.enquiry-card:hover {
  box-shadow: var(--shadow-md);
  border-color: #cbd5e1;
}

.enquiry-card.is-overdue {
  border-left: 4px solid var(--danger);
  background-color: #fffafb;
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.sender-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.sender-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}

.sender-phone {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.775rem;
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.message-preview {
  font-size: 0.85rem;
  color: #334155;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  background-color: #f8fafc;
  padding: 0.5rem 0.65rem;
  border-radius: var(--radius-sm);
  border-left: 2px solid #cbd5e1;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.4rem;
  border-top: 1px solid #f1f5f9;
}

.time-text {
  font-size: 0.75rem;
  color: #94a3b8;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-text-action {
  font-size: 0.775rem;
  font-weight: 600;
  color: var(--primary);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.btn-text-action:hover {
  color: var(--primary-hover);
  text-decoration: underline;
}

.quick-reply-section {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
