<template>
  <div class="pipeline-view single-window-container">
    <!-- Top toolbar: Filters, Search, KPIs, and Action CTA -->
    <div class="pipeline-toolbar card-box">
      <!-- Left: Channel Pills & SLA Overdue Filter Toggle -->
      <div class="toolbar-left">
        <div class="channel-pills">
          <button
            v-for="ch in channels"
            :key="ch.value"
            type="button"
            class="pill-btn"
            :class="{ active: store.selectedChannel === ch.value && !showOnlyOverdue }"
            @click="handleChannelSelect(ch.value)"
          >
            <span class="pill-label">{{ ch.label }}</span>
            <span class="pill-badge">{{ channelCounts[ch.value] || 0 }}</span>
          </button>

          <!-- SLA Overdue Quick Filter Toggle Pill -->
          <button
            v-if="store.overdueCount > 0"
            type="button"
            class="pill-btn overdue-pill-btn"
            :class="{ active: showOnlyOverdue }"
            @click="showOnlyOverdue = !showOnlyOverdue"
            title="Toggle leads overdue for follow-up (>48h)"
          >
            <span class="radar-dot"></span>
            <span class="pill-label">Overdue Only</span>
            <span class="pill-badge overdue-badge-num">{{ store.overdueCount }}</span>
          </button>
        </div>
      </div>

      <!-- Right: Search, Stats, and Quick Add CTA -->
      <div class="toolbar-right">
        <!-- Live KPI summary chips -->
        <div class="kpi-mini-group">
          <span class="kpi-chip" title="Total Active Leads">
            <strong>{{ displayedCount }}</strong> / {{ store.salesEnquiries.length }} Leads
          </span>
          <span class="kpi-chip won-chip" title="Total Won (Paid)">
            🏆 <strong>{{ (store.pipelineColumns['Paid'] || []).length }}</strong> Paid
          </span>
        </div>

        <!-- Search Input -->
        <div class="search-input-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="search-icon">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="store.searchQuery"
            type="text"
            placeholder="Search prospect, phone, query..."
            class="search-input"
          />
          <button
            v-if="store.searchQuery"
            type="button"
            class="clear-search"
            title="Clear search"
            @click="store.searchQuery = ''"
          >
            &times;
          </button>
        </div>

        <!-- Single Window Quick Add CTA -->
        <button
          type="button"
          class="btn-primary quick-add-btn"
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

    <!-- Active Filter Strip OR Compact Overdue Ribbon -->
    <div v-if="showOnlyOverdue" class="alert-ribbon overdue-active-ribbon">
      <div class="ribbon-left">
        <span class="radar-dot"></span>
        <span>
          Showing <strong>{{ displayedSalesEnquiries.length }}</strong> leads requiring urgent response (exceeded 48h SLA).
        </span>
      </div>
      <button type="button" class="btn-ribbon-action" @click="showOnlyOverdue = false">
        Show All Leads &times;
      </button>
    </div>

    <div v-else-if="store.overdueCount > 0" class="alert-ribbon overdue-prompt-ribbon">
      <div class="ribbon-left">
        <span class="radar-dot"></span>
        <span>
          <strong>48h SLA Notice:</strong> {{ store.overdueCount }} active leads have had no contact for over 48 hours.
        </span>
      </div>
      <div class="ribbon-right">
        <button type="button" class="btn-ribbon-filter" @click="showOnlyOverdue = true">
          Filter Overdue Leads &rarr;
        </button>
        <RouterLink to="/summary" class="ribbon-link">
          AI Weekly Report &rarr;
        </RouterLink>
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
        All ({{ displayedCount }})
      </button>
      <button
        v-for="status in columns"
        :key="status"
        type="button"
        class="tab-btn"
        :class="{ active: activeMobileTab === status }"
        @click="activeMobileTab = status"
      >
        {{ status }} ({{ (computedPipelineColumns[status] || []).length }})
      </button>
    </div>

    <!-- 5-Column Single-Window Pipeline Board -->
    <div class="pipeline-board">
      <template v-for="status in visibleColumns" :key="status">
        <PipelineColumn
          :status="status"
          :enquiries="computedPipelineColumns[status] || []"
          :loading="store.loading"
          @add="openQuickAddModal"
        />
      </template>
    </div>

    <!-- In-Place Cockpit Detail Modal -->
    <DetailModal
      v-if="store.activeModalEnquiry"
      :enquiry="store.activeModalEnquiry"
      @close="store.closeDetailModal"
    />

    <!-- In-Place Quick Add Single-Window Modal -->
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
const showOnlyOverdue = ref(false)

const columns = ['New', 'Contacted', 'Interested', 'Paid', 'Lost']

const channels = [
  { label: 'All', value: 'all' },
  { label: 'WhatsApp', value: 'whatsapp' },
  { label: 'Facebook', value: 'facebook' },
  { label: 'Website', value: 'website' },
  { label: 'Phone', value: 'phone' }
]

function handleChannelSelect(channelValue) {
  showOnlyOverdue.value = false
  store.selectedChannel = channelValue
}

function openQuickAddModal(status = 'New') {
  selectedColumnStatus.value = typeof status === 'string' ? status : 'New'
  showQuickAddModal.value = true
}

// Live counts per channel in sales enquiries
const channelCounts = computed(() => {
  const counts = { all: store.salesEnquiries.length, whatsapp: 0, facebook: 0, website: 0, phone: 0 }
  for (const e of store.salesEnquiries) {
    if (e.source && counts[e.source] !== undefined) {
      counts[e.source]++
    }
  }
  return counts
})

// Filtered leads taking into account channel, search, and overdue toggle
const displayedSalesEnquiries = computed(() => {
  let list = store.filteredSalesEnquiries
  if (showOnlyOverdue.value) {
    list = list.filter(e => store.isOverdue(e))
  }
  return list
})

const displayedCount = computed(() => displayedSalesEnquiries.value.length)

// Compute pipeline columns dynamically based on filtered leads
const computedPipelineColumns = computed(() => {
  const cols = { New: [], Contacted: [], Interested: [], Paid: [], Lost: [] }
  for (const enquiry of displayedSalesEnquiries.value) {
    if (cols[enquiry.status]) {
      cols[enquiry.status].push(enquiry)
    } else {
      cols.New.push(enquiry)
    }
  }
  return cols
})

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
/* ==========================================================================
   SINGLE WINDOW VIEWPORT LAYOUT
   ========================================================================== */
.single-window-container {
  flex: 1;
  min-height: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0.85rem 1.4rem 0.65rem;
  gap: 0.75rem;
  background-color: var(--bg-main);
}

/* Pipeline Toolbar */
.pipeline-toolbar {
  padding: 0.75rem 1.15rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  flex-shrink: 0;
  border-radius: var(--radius-md);
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.channel-pills {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.785rem;
  font-weight: 700;
  color: var(--text-muted);
  background-color: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  transition: all 0.15s ease;
  cursor: pointer;
  user-select: none;
}

.pill-btn:hover {
  color: var(--text-main);
  border-color: var(--primary);
  transform: translateY(-1px);
}

.pill-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #ffffff;
  border-color: var(--primary);
  box-shadow: 0 2px 8px var(--primary-glow);
}

.pill-badge {
  font-size: 0.68rem;
  font-weight: 800;
  padding: 0.05rem 0.4rem;
  border-radius: 9999px;
  background: var(--bg-surface);
  color: var(--text-muted);
}

.pill-btn.active .pill-badge {
  background: rgba(255, 255, 255, 0.22);
  color: #ffffff;
}

/* Overdue Pill Button */
.overdue-pill-btn {
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

.overdue-pill-btn.active {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.4);
}

.overdue-badge-num {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.overdue-pill-btn.active .overdue-badge-num {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* Radar Pulse Dot */
.radar-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ef4444;
  box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  animation: radarPulse 1.8s infinite;
  flex-shrink: 0;
}

@keyframes radarPulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* Toolbar Right */
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.kpi-mini-group {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.kpi-chip {
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-surface-elevated);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  white-space: nowrap;
}

.kpi-chip.won-chip {
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.08);
}

/* Search Wrapper */
.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  padding: 0.48rem 2rem 0.48rem 2.2rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--input-border);
  font-size: 0.825rem;
  width: 200px;
  outline: none;
  background-color: var(--input-bg);
  color: var(--input-text);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.search-input:focus {
  border-color: var(--primary);
  width: 250px;
  box-shadow: 0 0 0 3px var(--primary-glow);
}

.clear-search {
  position: absolute;
  right: 0.6rem;
  background: none;
  border: none;
  font-size: 1.1rem;
  color: var(--text-muted);
  cursor: pointer;
  line-height: 1;
}

.quick-add-btn {
  padding: 0.48rem 1.15rem;
  font-size: 0.825rem;
}

/* ==========================================================================
   ALERT RIBBON
   ========================================================================== */
.alert-ribbon {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.95rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  flex-shrink: 0;
  animation: fadeIn 0.2s ease;
}

.ribbon-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.overdue-active-ribbon {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

.overdue-prompt-ribbon {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.ribbon-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.btn-ribbon-filter {
  background: none;
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.btn-ribbon-filter:hover {
  background: #ef4444;
  color: #ffffff;
}

.btn-ribbon-action {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.ribbon-link {
  color: #ef4444;
  font-weight: 800;
  text-decoration: underline;
  font-size: 0.76rem;
}

/* Mobile Tabs */
.mobile-column-tabs {
  display: none;
  gap: 0.35rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  flex-shrink: 0;
}

.tab-btn {
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
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

/* ==========================================================================
   PIPELINE BOARD CONTAINER (100% Flex Viewport Fit)
   ========================================================================== */
.pipeline-board {
  display: flex;
  gap: 0.85rem;
  overflow-x: auto;
  overflow-y: hidden;
  flex: 1;
  min-height: 0;
  height: 100%;
  padding-bottom: 0.25rem;
}

/* Custom Scrollbar for horizontal board */
.pipeline-board::-webkit-scrollbar {
  height: 5px;
}
.pipeline-board::-webkit-scrollbar-track {
  background: transparent;
}
.pipeline-board::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}
.pipeline-board::-webkit-scrollbar-thumb:hover {
  background: var(--primary);
}

@media (max-width: 900px) {
  .mobile-column-tabs {
    display: flex;
  }

  .pipeline-board {
    overflow-x: hidden;
  }

  .single-window-container {
    padding: 0.65rem 0.85rem;
  }

  .search-input {
    width: 100%;
  }

  .search-input:focus {
    width: 100%;
  }
}
</style>
