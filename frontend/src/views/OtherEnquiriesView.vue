<template>
  <div class="other-view">
    <div class="view-header">
      <div>
        <h2 class="view-title">Other Enquiries (Non-Sales)</h2>
        <p class="view-subtitle">Support tickets, job seeker applications, and spam isolated to keep the sales pipeline clean.</p>
      </div>

      <!-- Type Filter Tabs -->
      <div class="type-filter-tabs">
        <button
          v-for="t in typeTabs"
          :key="t.value"
          type="button"
          class="tab-btn"
          :class="{ active: currentTab === t.value }"
          @click="currentTab = t.value"
        >
          {{ t.label }}
          <span class="tab-count">{{ getTabCount(t.value) }}</span>
        </button>
      </div>
    </div>

    <!-- Skeleton Loading State -->
    <div v-if="store.loading" class="cards-grid">
      <div v-for="n in 4" :key="n" class="other-card card-box">
        <div class="skeleton-header">
          <div class="skeleton-avatar skeleton-pulse"></div>
          <div class="skeleton-meta">
            <div class="skeleton-line sm skeleton-pulse"></div>
            <div class="skeleton-line xs skeleton-pulse"></div>
          </div>
        </div>
        <div class="skeleton-line full skeleton-pulse"></div>
        <div class="skeleton-line md skeleton-pulse"></div>
        <div class="skeleton-footer">
          <div class="skeleton-pill skeleton-pulse"></div>
        </div>
      </div>
    </div>

    <!-- Enquiries Cards Grid -->
    <div v-else-if="filteredList.length > 0" class="cards-grid">
      <div
        v-for="item in filteredList"
        :key="item.id"
        class="other-card card-box"
        :class="`type-${item.enquiry_type}`"
        @click="openModal(item)"
      >
        <div class="card-header">
          <div class="user-block">
            <div class="avatar-sm">
              {{ (item.name ? item.name[0] : 'U').toUpperCase() }}
            </div>
            <div>
              <h3 class="user-name">{{ item.name || 'Anonymous' }}</h3>
              <span v-if="item.phone" class="user-phone font-mono">
                <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                </svg>
                {{ item.phone }}
              </span>
            </div>
          </div>

          <div class="badges-group">
            <span class="badge" :class="`badge-${item.enquiry_type}`">
              {{ formatType(item.enquiry_type) }}
            </span>
            <span class="badge" :class="getChannelBadgeClass(item.source)">
              {{ item.source }}
            </span>
          </div>
        </div>

        <div class="message-bubble">
          <p class="message-content">{{ item.message }}</p>
        </div>

        <div class="card-footer" @click.stop>
          <span class="date-text">{{ formatDate(item.created_at) }}</span>
          <button
            v-if="item.enquiry_type !== 'spam'"
            type="button"
            class="btn-suggest"
            @click="activeReplyId = activeReplyId === item.id ? null : item.id"
          >
            {{ activeReplyId === item.id ? 'Close Reply' : 'Suggested Reply' }}
          </button>
        </div>

        <!-- Inline Reply Section if toggled -->
        <div v-if="activeReplyId === item.id" class="reply-toggle-area" @click.stop>
          <ReplyBox
            :reply-text="item.ai_reply || ''"
            :language="item.language"
            @update:reply-text="item.ai_reply = $event"
          />
        </div>
      </div>
    </div>

    <div v-else class="empty-state card-box">
      <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect width="20" height="16" x="2" y="4" rx="2"/>
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
      </svg>
      <h3>No {{ currentTab === 'all' ? '' : currentTab }} enquiries found</h3>
      <p>Any non-sales messages automatically filter to this section.</p>
    </div>

    <!-- Detail Modal -->
    <DetailModal
      v-if="store.activeModalEnquiry"
      :enquiry="store.activeModalEnquiry"
      @close="store.closeDetailModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import DetailModal from '../components/DetailModal.vue'
import ReplyBox from '../components/ReplyBox.vue'
import { formatDate, getChannelBadgeClass } from '../utils/format'

const store = useEnquiriesStore()

const currentTab = ref('all')
const activeReplyId = ref(null)

const typeTabs = [
  { label: 'All Non-Sales', value: 'all' },
  { label: 'Support Tickets', value: 'support' },
  { label: 'Job Seekers', value: 'job_seeker' },
  { label: 'Spam Filtered', value: 'spam' }
]

function getTabCount(type) {
  if (type === 'all') return store.otherEnquiries.length
  return store.otherEnquiries.filter(e => e.enquiry_type === type).length
}

const filteredList = computed(() => {
  if (currentTab.value === 'all') {
    return store.otherEnquiries
  }
  return store.otherEnquiries.filter(e => e.enquiry_type === currentTab.value)
})

function formatType(type) {
  switch (type) {
    case 'support': return 'Support'
    case 'job_seeker': return 'Job Seeker'
    case 'spam': return 'Spam'
    default: return type
  }
}

function openModal(item) {
  store.openDetailModal(item)
}

onMounted(() => {
  store.fetchAll()
})
</script>

<style scoped>
.other-view {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.view-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.view-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.type-filter-tabs {
  display: flex;
  gap: 0.4rem;
  background: var(--bg-surface-elevated);
  padding: 0.3rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  flex-wrap: wrap;
}

.tab-btn {
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.45rem;
  transition: all 0.15s;
}

.tab-btn:hover {
  color: var(--text-main);
}

.tab-btn.active {
  background: var(--bg-surface);
  color: var(--text-main);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-count {
  font-size: 0.7rem;
  background: var(--bg-surface-elevated);
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.15rem;
}

.other-card {
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  cursor: pointer;
  border-left: 3px solid var(--border-color);
  transition: all 0.2s ease;
}

.other-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--card-shadow-hover);
}

.other-card.type-support {
  border-left-color: #3b82f6;
}

.other-card.type-job_seeker {
  border-left-color: #10b981;
}

.other-card.type-spam {
  border-left-color: #ef4444;
  opacity: 0.75;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.user-block {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
}

.user-name {
  font-size: 0.925rem;
  font-weight: 700;
  color: var(--text-main);
}

.user-phone {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.badges-group {
  display: flex;
  gap: 0.35rem;
}

.badge-support {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.badge-job_seeker {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-spam {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.message-bubble {
  background: var(--bg-surface-elevated);
  padding: 0.75rem 0.9rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.message-content {
  font-size: 0.85rem;
  color: var(--text-main);
  line-height: 1.5;
  white-space: pre-wrap;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.35rem;
}

.date-text {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.btn-suggest {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}

.btn-suggest:hover {
  background: var(--primary);
  color: #fff;
}

.reply-toggle-area {
  margin-top: 0.5rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1.5rem;
  gap: 0.75rem;
  color: var(--text-muted);
  text-align: center;
}

.empty-state h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}

/* Skeleton styling */
.skeleton-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.skeleton-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  flex-shrink: 0;
}

.skeleton-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.skeleton-line {
  height: 10px;
  border-radius: 4px;
}

.skeleton-line.xs { width: 40%; height: 8px; }
.skeleton-line.sm { width: 60%; }
.skeleton-line.md { width: 85%; }
.skeleton-line.full { width: 100%; }

.skeleton-footer {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.skeleton-pill {
  width: 80px;
  height: 20px;
  border-radius: 9999px;
}
</style>
