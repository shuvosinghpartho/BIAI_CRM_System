<template>
  <div
    class="enquiry-card card-box"
    :class="{ 'is-overdue': overdue }"
    @click="openModal"
  >
    <!-- Card Header: Avatar, Name, Phone & Overdue Badge -->
    <div class="card-top">
      <div class="sender-info">
        <div class="sender-header-line">
          <div class="avatar-sm">
            {{ (enquiry.name ? enquiry.name[0] : 'U').toUpperCase() }}
          </div>
          <div class="sender-text-group">
            <h4 class="sender-name">{{ enquiry.name || 'Anonymous Prospect' }}</h4>
            <span v-if="enquiry.phone" class="sender-phone font-mono">
              <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
              {{ enquiry.phone }}
            </span>
          </div>
        </div>
      </div>
      <OverdueBadge :overdue="overdue" />
    </div>

    <!-- Badges Row -->
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

    <!-- Message Body Bubble -->
    <div class="message-bubble">
      <p class="message-text">"{{ enquiry.message }}"</p>
    </div>

    <!-- Card Footer: Time Ago & Quick Status Dropdown -->
    <div class="card-footer" @click.stop>
      <span class="time-meta">{{ formatTimeAgo(enquiry.created_at) }}</span>
      <StatusSelect
        :model-value="enquiry.status"
        @change="handleStatusChange"
      />
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
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  cursor: pointer;
  border-radius: var(--radius-md);
  position: relative;
}

.enquiry-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
}

.enquiry-card.is-overdue {
  border-left: 4px solid var(--danger);
  background: var(--danger-bg);
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.sender-header-line {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.avatar-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--bg-surface-elevated), var(--border-color));
  color: var(--text-main);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 800;
  flex-shrink: 0;
}

.sender-text-group {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.sender-name {
  font-size: 0.925rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.25;
}

.sender-phone {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.message-bubble {
  background-color: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  padding: 0.65rem 0.75rem;
  border-radius: var(--radius-sm);
}

.message-text {
  font-size: 0.825rem;
  color: var(--text-main);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-style: italic;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.45rem;
  border-top: 1px solid var(--border-color);
}

.time-meta {
  font-size: 0.725rem;
  font-weight: 600;
  color: var(--text-muted);
}
</style>
