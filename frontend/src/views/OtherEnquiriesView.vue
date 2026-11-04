<template>
  <div class="other-view">
    <div class="view-header">
      <div>
        <h2 class="view-title">Other Enquiries (Non-Sales)</h2>
        <p class="view-subtitle">Support tickets, job seeker applications, and spam filtered away from the main sales pipeline.</p>
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

    <!-- Enquiries List -->
    <div v-if="filteredList.length > 0" class="cards-grid">
      <div
        v-for="item in filteredList"
        :key="item.id"
        class="other-card"
        :class="`type-${item.enquiry_type}`"
      >
        <div class="card-header">
          <div class="user-block">
            <h3 class="user-name">{{ item.name || 'Anonymous' }}</h3>
            <span v-if="item.phone" class="user-phone">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
              </svg>
              {{ item.phone }}
            </span>
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

        <p class="message-content">
          {{ item.message }}
        </p>

        <div class="card-footer">
          <span class="date-text">{{ formatDate(item.created_at) }}</span>
          <button
            v-if="item.enquiry_type !== 'spam'"
            type="button"
            class="btn-suggest"
            @click="activeReplyId = activeReplyId === item.id ? null : item.id"
          >
            {{ activeReplyId === item.id ? 'Close' : 'Generate Reply' }}
          </button>
        </div>

        <!-- Inline Reply Section if toggled -->
        <div v-if="activeReplyId === item.id" class="reply-toggle-area">
          <ReplyBox
            :reply-text="item.ai_reply || ''"
            :language="item.language"
            @update:reply-text="item.ai_reply = $event"
          />
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <rect width="20" height="16" x="2" y="4" rx="2"/>
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
      </svg>
      <h3>No {{ currentTab === 'all' ? '' : currentTab }} enquiries found</h3>
      <p>Any non-sales messages automatically filter to this section.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import ReplyBox from '../components/ReplyBox.vue'
import { formatDate, getChannelBadgeClass } from '../utils/format'

const store = useEnquiriesStore()
const currentTab = ref('all')
const activeReplyId = ref(null)

const typeTabs = [
  { label: 'All Non-Sales', value: 'all' },
  { label: 'Support Issues', value: 'support' },
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
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
}

.view-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.type-filter-tabs {
  display: flex;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.25rem;
  border-radius: var(--radius-sm);
}

.tab-btn {
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.15s;
}

.tab-btn.active {
  background: #ffffff;
  color: var(--text-main);
  box-shadow: var(--shadow-sm);
}

.tab-count {
  background: #e2e8f0;
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  font-size: 0.725rem;
}

.tab-btn.active .tab-count {
  background: var(--primary);
  color: #ffffff;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.25rem;
}

.other-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.other-card.type-support {
  border-left: 4px solid #f59e0b;
}

.other-card.type-job_seeker {
  border-left: 4px solid #8b5cf6;
}

.other-card.type-spam {
  border-left: 4px solid #ef4444;
  opacity: 0.85;
}

.badge-support {
  background-color: #fef3c7;
  color: #b45309;
}

.badge-job_seeker {
  background-color: #f3e8ff;
  color: #7e22ce;
}

.badge-spam {
  background-color: #fee2e2;
  color: #b91c1c;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.user-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}

.user-phone {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.775rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.badges-group {
  display: flex;
  gap: 0.35rem;
}

.message-content {
  font-size: 0.875rem;
  color: #334155;
  line-height: 1.5;
  background-color: #f8fafc;
  padding: 0.75rem;
  border-radius: var(--radius-sm);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f1f5f9;
  padding-top: 0.5rem;
}

.date-text {
  font-size: 0.775rem;
  color: #94a3b8;
}

.btn-suggest {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--primary);
}

.btn-suggest:hover {
  text-decoration: underline;
}

.empty-state {
  text-align: center;
  padding: 4rem 1rem;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
</style>
