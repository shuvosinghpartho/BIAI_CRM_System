<template>
  <div class="status-select-wrapper" @click.stop>
    <select
      :value="modelValue"
      :class="['status-select', `status-${modelValue.toLowerCase()}`]"
      :disabled="updating"
      @change="handleChange($event.target.value)"
    >
      <option value="New">New</option>
      <option value="Contacted">Contacted</option>
      <option value="Interested">Interested</option>
      <option value="Paid">Paid</option>
      <option value="Lost">Lost</option>
    </select>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])
const updating = ref(false)

function handleChange(val) {
  emit('update:modelValue', val)
  emit('change', val)
}
</script>

<style scoped>
.status-select-wrapper {
  display: inline-block;
}

.status-select {
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-sm);
  font-size: 0.775rem;
  font-weight: 600;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  cursor: pointer;
  outline: none;
  transition: all 0.15s ease;
}

.status-select:hover {
  border-color: var(--primary);
}

.status-new {
  color: #2563eb;
  background-color: rgba(37, 99, 235, 0.12);
  border-color: rgba(37, 99, 235, 0.3);
}

.status-contacted {
  color: #d97706;
  background-color: rgba(217, 119, 6, 0.12);
  border-color: rgba(217, 119, 6, 0.3);
}

.status-interested {
  color: #7c3aed;
  background-color: rgba(124, 58, 237, 0.12);
  border-color: rgba(124, 58, 237, 0.3);
}

.status-paid {
  color: #16a34a;
  background-color: rgba(22, 163, 74, 0.12);
  border-color: rgba(22, 163, 74, 0.3);
}

.status-lost {
  color: var(--text-muted);
  background-color: var(--bg-surface-elevated);
  border-color: var(--border-color);
}
</style>
