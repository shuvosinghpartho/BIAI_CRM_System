<template>
  <div class="pipeline-view">
    <!-- Top toolbar: Filters, Search, and Stats -->
    <div class="pipeline-toolbar">
      <div class="filter-group">
        <label class="filter-label">Filter Channel:</label>
        <div class="channel-pills">
          <button
            v-for="ch in channels"
            :key="ch.value"
            type="button"
            class="pill-btn"
            :class="{ active: store.selectedChannel === ch.value }"
            @click="store.selectedChannel = ch.value"
          >
            {{ ch.label }}
          </button>
        </div>
      </div>

      <div class="search-and-cta">
        <div class="search-input-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="search-icon">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="store.searchQuery"
            type="text"
            placeholder="Search leads, phone, text..."
            class="search-input"
          />
          <button
            v-if="store.searchQuery"
            type="button"
            class="clear-search"
            @click="store.searchQuery = ''"
          >
            &times;
          </button>
        </div>

        <RouterLink to="/add" class="btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          New Enquiry
        </RouterLink>
      </div>
    </div>

    <!-- Overdue Alert Banner if overdue enquiries exist -->
    <div v-if="store.overdueCount > 0" class="overdue-alert-banner">
      <div class="banner-left">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>
          <strong>Follow-up Alert:</strong> {{ store.overdueCount }} active sales leads have had no contact for 48+ hours.
        </span>
      </div>
      <RouterLink to="/summary" class="banner-link">
        Review Overdue Leads &rarr;
      </RouterLink>
    </div>

    <!-- 5-Column Pipeline Board -->
    <div class="pipeline-board">
      <PipelineColumn
        v-for="status in columns"
        :key="status"
        :status="status"
        :enquiries="store.pipelineColumns[status] || []"
      />
    </div>

    <!-- Detail Slide-over Modal -->
    <DetailModal
      v-if="store.activeModalEnquiry"
      :enquiry="store.activeModalEnquiry"
      @close="store.closeDetailModal"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useEnquiriesStore } from '../stores/enquiries'
import PipelineColumn from '../components/PipelineColumn.vue'
import DetailModal from '../components/DetailModal.vue'

const store = useEnquiriesStore()

const columns = ['New', 'Contacted', 'Interested', 'Paid', 'Lost']

const channels = [
  { label: 'All Channels', value: 'all' },
  { label: 'WhatsApp', value: 'whatsapp' },
  { label: 'Facebook', value: 'facebook' },
  { label: 'Website', value: 'website' },
  { label: 'Phone', value: 'phone' }
]

onMounted(() => {
  store.fetchAll()
})
</script>

<style scoped>
.pipeline-view {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  flex: 1;
}

.pipeline-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  background: var(--bg-surface);
  padding: 0.85rem 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filter-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
}

.channel-pills {
  display: flex;
  gap: 0.35rem;
}

.pill-btn {
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  background-color: var(--bg-surface-elevated);
  transition: all 0.15s ease;
}

.pill-btn:hover {
  color: var(--text-main);
  background-color: var(--border-color);
}

.pill-btn.active {
  background-color: var(--primary);
  color: #ffffff;
}

.search-and-cta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  color: var(--text-muted);
}

.search-input {
  padding: 0.5rem 2rem 0.5rem 2.25rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  font-size: 0.85rem;
  width: 240px;
  outline: none;
  background-color: var(--input-bg);
  color: var(--text-main);
  transition: all 0.15s;
}

.search-input:focus {
  border-color: var(--primary);
  width: 280px;
}

.clear-search {
  position: absolute;
  right: 0.6rem;
  font-size: 1.1rem;
  color: var(--text-muted);
  line-height: 1;
}

.overdue-alert-banner {
  background-color: var(--danger-light);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: var(--danger);
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.875rem;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.banner-link {
  color: var(--danger);
  font-weight: 700;
  text-decoration: underline;
}

.pipeline-board {
  display: flex;
  gap: 1.15rem;
  overflow-x: auto;
  padding-bottom: 1rem;
  flex: 1;
}
</style>
