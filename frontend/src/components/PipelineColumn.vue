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
  min-width: 280px;
  max-width: 340px;
  background-color: #f1f5f9;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 170px);
  border: 1px solid #e2e8f0;
}

.column-header {
  padding: 1rem 1.15rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
  background: #ffffff;
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
}

.col-title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.col-new .status-indicator { background-color: #3b82f6; }
.col-contacted .status-indicator { background-color: #f59e0b; }
.col-interested .status-indicator { background-color: #8b5cf6; }
.col-paid .status-indicator { background-color: #10b981; }
.col-lost .status-indicator { background-color: #94a3b8; }

.status-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}

.count-badge {
  background-color: #f1f5f9;
  color: #475569;
  font-size: 0.775rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 9999px;
  border: 1px solid #e2e8f0;
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
  padding: 2.5rem 1rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.85rem;
  border: 1px dashed #cbd5e1;
  border-radius: var(--radius-md);
  margin: 0.5rem 0;
}
</style>
