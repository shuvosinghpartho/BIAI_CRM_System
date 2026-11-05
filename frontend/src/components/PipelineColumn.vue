<template>
  <div class="pipeline-column" :class="`col-${status.toLowerCase()}`">
    <div class="column-header">
      <div class="col-title-group">
        <span class="status-indicator"></span>
        <h3 class="status-title">{{ status }}</h3>
      </div>
      <div class="header-badges">
        <span class="count-badge">{{ enquiries.length }}</span>
        <button
          type="button"
          class="btn-column-add"
          :title="`Add new lead to ${status}`"
          @click.stop="$emit('add', status)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="cards-container">
      <!-- Skeleton Loading State -->
      <template v-if="loading">
        <div v-for="n in 3" :key="n" class="skeleton-card">
          <div class="skeleton-header">
            <div class="skeleton-avatar skeleton-pulse"></div>
            <div class="skeleton-meta">
              <div class="skeleton-line sm skeleton-pulse"></div>
              <div class="skeleton-line xs skeleton-pulse"></div>
            </div>
          </div>
          <div class="skeleton-line md skeleton-pulse"></div>
          <div class="skeleton-line full skeleton-pulse"></div>
          <div class="skeleton-footer">
            <div class="skeleton-pill skeleton-pulse"></div>
            <div class="skeleton-pill sm skeleton-pulse"></div>
          </div>
        </div>
      </template>

      <!-- Loaded Cards -->
      <template v-else-if="enquiries.length > 0">
        <TransitionGroup name="card-anim" tag="div" class="cards-transition-wrap">
          <EnquiryCard
            v-for="enquiry in enquiries"
            :key="enquiry.id"
            :enquiry="enquiry"
          />
        </TransitionGroup>
      </template>

      <!-- Empty State -->
      <div v-else class="empty-column-state">
        <div class="empty-icon-wrap">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
        </div>
        <p>No enquiries in {{ status }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import EnquiryCard from './EnquiryCard.vue'

defineProps({
  status: {
    type: String,
    required: true
  },
  enquiries: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['add'])
</script>

<style scoped>
.header-badges {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.btn-column-add {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.btn-column-add:hover {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  transform: scale(1.08);
}

<style scoped>
.pipeline-column {
  flex: 1;
  min-width: 290px;
  max-width: 350px;
  background-color: var(--column-bg);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 170px);
  border: 1px solid var(--border-color);
  box-shadow: var(--card-shadow);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.pipeline-column:hover {
  border-color: var(--border-hover);
}

.column-header {
  padding: 0.95rem 1.15rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-surface);
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
}

.col-title-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.col-new .status-indicator { background-color: var(--status-new); box-shadow: 0 0 8px var(--status-new); }
.col-contacted .status-indicator { background-color: var(--status-contacted); box-shadow: 0 0 8px var(--status-contacted); }
.col-interested .status-indicator { background-color: var(--status-interested); box-shadow: 0 0 8px var(--status-interested); }
.col-paid .status-indicator { background-color: var(--status-paid); box-shadow: 0 0 8px var(--status-paid); }
.col-lost .status-indicator { background-color: var(--status-lost); }

.status-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.01em;
}

.count-badge {
  background-color: var(--bg-surface-elevated);
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.15rem 0.55rem;
  border-radius: 9999px;
  border: 1px solid var(--border-color);
}

.cards-container {
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  overflow-y: auto;
  flex: 1;
}

.cards-transition-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* Card animations */
.card-anim-enter-active,
.card-anim-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.card-anim-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.97);
}
.card-anim-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Skeleton Loading Cards */
.skeleton-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.skeleton-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.skeleton-avatar {
  width: 32px;
  height: 32px;
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
  width: 60px;
  height: 18px;
  border-radius: 9999px;
}

.skeleton-pill.sm { width: 45px; }

.empty-column-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  gap: 0.6rem;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: center;
}

.empty-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-surface-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed var(--border-color);
  color: var(--text-muted);
}
</style>
