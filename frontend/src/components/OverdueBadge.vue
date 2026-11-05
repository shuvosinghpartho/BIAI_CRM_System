<template>
  <span v-if="overdue" class="badge-overdue-pill" title="No follow-up in the last 48 hours">
    <span class="pulsing-radar-dot"></span>
    <span class="overdue-text">48h+ Overdue</span>
  </span>
</template>

<script setup>
defineProps({
  overdue: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.badge-overdue-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(239, 68, 68, 0.14);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.4);
  padding: 0.18rem 0.55rem;
  border-radius: 9999px;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.pulsing-radar-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ef4444;
  box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  animation: radarPulse 1.8s infinite;
  flex-shrink: 0;
}

@keyframes radarPulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 5px rgba(239, 68, 68, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.overdue-text {
  line-height: 1;
}
</style>
