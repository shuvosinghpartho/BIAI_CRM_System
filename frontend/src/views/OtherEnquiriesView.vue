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

    <!-- Enquiries Cards Grid -->
    <div v-if="filteredList.length > 0" class="cards-grid">
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
import ReplyBox from '../components/ReplyBox.vue'
import DetailModal from '../components/DetailModal.vue'
import { formatDate, getChannelBadgeClass } from '../utils/format'

const store = useEnquiriesStore()
const currentTab = ref('all')
const activeReplyId = ref(null)

const typeTabs = [
  { label: 'All Non-Sales', value: 'all' },
  { label: 'Support', value: 'support' },
  { label: 'Job Seekers', value: 'job_seeker' },
  { label: 'Spam', value: 'spam' }
]

onMounted(() => {
  store.fetchAll()
})

const filteredList = computed(() => {
  const others = store.otherEnquiries
  if (currentTab.value === 'all') return others
  return others.filter(e => e.enquiry_type === currentTab.value)
})

function getTabCount(type) {
  if (type === 'all') return store.otherEnquiries.length
  return store.otherEnquiries.filter(e => e.enquiry_type === type).length
}

function formatType(type) {
  if (type === 'job_seeker') return 'Job Seeker'
  return type ? type.toUpperCase() : 'OTHER'
}

function openModal(enquiry) {
  store.openDetailModal(enquiry)
}
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
  align-items: center;
  justify-content: space-between;
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
}

.type-filter-tabs {
  display: flex;
  gap: 0.4rem;
  background: var(--bg-surface-elevated);
  padding: 0.3rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
}

.tab-btn {
  padding: 0.35rem 0.95rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  transition: all 0.15s;
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  box-shadow: 0 2px 8px var(--primary-glow);
}

.tab-count {
  background: var(--border-color);
  padding: 0.1rem 0.45rem;
  border-radius: var(--radius-full);
  font-size: 0.725rem;
  color: var(--text-main);
}

.tab-btn.active .tab-count {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.25rem;
}

.other-card {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  cursor: pointer;
  border-radius: var(--radius-md);
}

.other-card:hover {
  transform: translateY(-2px);
}

.other-card.type-support {
  border-left: 4px solid var(--warning);
}

.other-card.type-job_seeker {
  border-left: 4px solid #a855f7;
}

.other-card.type-spam {
  border-left: 4px solid var(--danger);
  opacity: 0.85;
}

.badge-support {
  background-color: var(--warning-bg);
  color: var(--warning);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-job_seeker {
  background-color: rgba(168, 85, 247, 0.15);
  color: #a855f7;
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.badge-spam {
  background-color: var(--danger-bg);
  color: var(--danger);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
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
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
}

.user-phone {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.badges-group {
  display: flex;
  gap: 0.35rem;
}

.message-bubble {
  background-color: var(--bg-surface-elevated);
  padding: 0.75rem 0.85rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.message-content {
  font-size: 0.85rem;
  color: var(--text-main);
  line-height: 1.5;
  font-style: italic;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-color);
  padding-top: 0.5rem;
}

.date-text {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.btn-suggest {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--primary);
}

.btn-suggest:hover {
  text-decoration: underline;
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
</style>
