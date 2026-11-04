<template>
  <div
    class="enquiry-card"
    :class="{ 'is-overdue': overdue }"
    @click="openModal"
  >
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
    <div class="card-footer" @click.stop>
      <div class="time-meta">
        <span class="time-text">{{ formatTimeAgo(enquiry.created_at) }}</span>
      </div>
      <StatusSelect
        :model-value="enquiry.status"
        @change="handleStatusChange"
      />
    </div>

    <!-- Quick action links -->
    <div class="card-actions" @click.stop>
      <button
        type="button"
        class="btn-text-action"
        @click="openModal"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="16" x2="12" y2="12"/>
          <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        Details & Reply
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import StatusSelect from './StatusSelect.vue'
import OverdueBadge from './OverdueBadge.vue'
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
const overdue = computed(() => store.isOverdue(props.enquiry))

async function handleStatusChange(newStatus) {
  await store.updateStatus(props.enquiry.id, newStatus)
}

function openModal() {
  store.openDetailModal(props.enquiry)
}
</script>

<style scoped>
.enquiry-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.enquiry-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
  transform: translateY(-2px);
}

.enquiry-card.is-overdue {
  border-left: 4px solid var(--danger);
  background: var(--danger-light);
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
  color: var(--text-main);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  background-color: var(--bg-surface-elevated);
  padding: 0.5rem 0.65rem;
  border-radius: var(--radius-sm);
  border-left: 2px solid var(--border-color);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.4rem;
  border-top: 1px solid var(--border-color);
}

.time-text {
  font-size: 0.75rem;
  color: var(--text-muted);
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
</style>
