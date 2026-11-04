<template>
  <div class="pipeline-column" :class="`col-${status.toLowerCase()}`">
    <div class="column-header">
      <div class="col-title-group">
        <span class="status-indicator"></span>
        <h3 class="status-title">{{ status }}</h3>
      </div>
      <span class="count-badge">{{ enquiries.length }}</span>
    </div>

    <div class="cards-container">
      <template v-if="enquiries.length > 0">
        <EnquiryCard
          v-for="enquiry in enquiries"
          :key="enquiry.id"
          :enquiry="enquiry"
        />
      </template>
      <div v-else class="empty-column-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <line x1="8" y1="12" x2="16" y2="12"/>
        </svg>
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
  }
})
</script>

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
}

.column-header {
  padding: 1rem 1.15rem;
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
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
}

.cards-container {
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  overflow-y: auto;
  flex: 1;
}

.empty-column-state {
  padding: 3rem 1rem;
  text-align: center;
  color: var(--text-dim);
  font-size: 0.825rem;
  border: 1px dashed var(--border-color);
  border-radius: var(--radius-md);
  margin: 0.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
</style>
