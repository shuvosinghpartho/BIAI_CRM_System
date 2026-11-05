<template>
  <div class="pipeline-view">
    <!-- Top toolbar: Filters, Search, and Action CTA -->
    <div class="pipeline-toolbar card-box">
      <div class="filter-group">
        <span class="filter-label">Filter Channel:</span>
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
            placeholder="Search leads, phone, query..."
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

        <!-- Single Window Quick Add CTA -->
        <button
          type="button"
          class="btn-primary"
          @click="openQuickAddModal('New')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>Quick Add Lead</span>
        </button>
      </div>
    </div>

    <!-- Mobile Column Switcher (Visible on small screens) -->
    <div class="mobile-column-tabs">
      <button
        type="button"
        class="tab-btn"
        :class="{ active: activeMobileTab === 'all' }"
        @click="activeMobileTab = 'all'"
      >
        All ({{ store.filteredSalesEnquiries.length }})
      </button>
      <button
        v-for="status in columns"
        :key="status"
        type="button"
        class="tab-btn"
        :class="{ active: activeMobileTab === status }"
        @click="activeMobileTab = status"
      >
        {{ status }} ({{ (store.pipelineColumns[status] || []).length }})
      </button>
    </div>

    <!-- Overdue Alert Banner if overdue enquiries exist -->
    <div v-if="store.overdueCount > 0" class="overdue-alert-banner">
      <div class="banner-left">
        <div class="alert-icon-circle">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <span>
          <strong>Follow-up SLA Alert:</strong> {{ store.overdueCount }} active leads have had no contact for over 48 hours.
        </span>
      </div>
      <RouterLink to="/summary" class="banner-link">
        Resolve Now &rarr;
      </RouterLink>
    </div>

    <!-- 5-Column Pipeline Board -->
    <div class="pipeline-board">
      <template v-for="status in visibleColumns" :key="status">
        <PipelineColumn
          :status="status"
          :enquiries="store.pipelineColumns[status] || []"
          :loading="store.loading"
          @add="openQuickAddModal"
        />
      </template>
    </div>

    <!-- Slide-over / Modal Detail View -->
    <DetailModal
      v-if="store.activeModalEnquiry"
      :enquiry="store.activeModalEnquiry"
      @close="store.closeDetailModal"
    />

    <!-- Quick Add Single-Window Modal -->
    <QuickAddModal
      v-if="showQuickAddModal"
      :initial-status="selectedColumnStatus"
      @close="showQuickAddModal = false"
      @saved="store.fetchAll"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useEnquiriesStore } from '../stores/enquiries'
import PipelineColumn from '../components/PipelineColumn.vue'
import DetailModal from '../components/DetailModal.vue'
import QuickAddModal from '../components/QuickAddModal.vue'

const store = useEnquiriesStore()
const showQuickAddModal = ref(false)
const selectedColumnStatus = ref('New')
const activeMobileTab = ref('all')

function openQuickAddModal(status = 'New') {
  selectedColumnStatus.value = typeof status === 'string' ? status : 'New'
  showQuickAddModal.value = true
}

const columns = ['New', 'Contacted', 'Interested', 'Paid', 'Lost']

const channels = [
  { label: 'All', value: 'all' },
  { label: 'WhatsApp', value: 'whatsapp' },
  { label: 'Facebook', value: 'facebook' },
  { label: 'Website', value: 'website' },
  { label: 'Phone', value: 'phone' }
]

const visibleColumns = computed(() => {
  if (activeMobileTab.value === 'all') {
    return columns
  }
  return [activeMobileTab.value]
})

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
  padding: 1rem 1.25rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
}

.channel-pills {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.pill-btn {
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  background-color: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  transition: all 0.15s ease;
  cursor: pointer;
}

.pill-btn:hover {
  color: var(--text-main);
  border-color: var(--primary);
}

.pill-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  border-color: var(--primary);
  box-shadow: 0 2px 8px var(--primary-glow);
}

.search-and-cta {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.85rem;
  color: var(--text-muted);
}

.search-input {
  padding: 0.55rem 2rem 0.55rem 2.35rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  font-size: 0.85rem;
  width: 220px;
  outline: none;
  background-color: var(--input-bg);
  color: var(--input-text);
  transition: all 0.2s;
}

.search-input:focus {
  border-color: var(--primary);
  width: 260px;
  box-shadow: 0 0 0 3px var(--primary-glow);
}

.clear-search {
  position: absolute;
  right: 0.65rem;
  background: none;
  border: none;
  font-size: 1.15rem;
  color: var(--text-muted);
  cursor: pointer;
  line-height: 1;
}

/* Mobile column tabs */
.mobile-column-tabs {
  display: none;
  gap: 0.4rem;
  overflow-x: auto;
  padding-bottom: 0.35rem;
}

.tab-btn {
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 700;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s;
}

.tab-btn.active {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}

.overdue-alert-banner {
  background-color: var(--danger-bg);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: var(--danger);
  padding: 0.85rem 1.25rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.15);
}

.alert-icon-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.banner-link {
  color: var(--danger);
  font-weight: 800;
  text-decoration: underline;
  white-space: nowrap;
}

.pipeline-board {
  display: flex;
  gap: 1.25rem;
  overflow-x: auto;
  padding-bottom: 1.25rem;
  flex: 1;
}

@media (max-width: 900px) {
  .mobile-column-tabs {
    display: flex;
  }

  .pipeline-board {
    overflow-x: hidden;
  }

  .pipeline-view {
    padding: 1rem;
  }

  .search-input {
    width: 100%;
  }

  .search-input:focus {
    width: 100%;
  }
}
</style>
