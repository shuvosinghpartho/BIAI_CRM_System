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
  background-color: #fff;
  cursor: pointer;
  outline: none;
  transition: all 0.15s ease;
}

.status-select:hover {
  border-color: #94a3b8;
}

.status-new {
  color: #2563eb;
  background-color: #eff6ff;
  border-color: #bfdbfe;
}

.status-contacted {
  color: #d97706;
  background-color: #fffbeb;
  border-color: #fde68a;
}

.status-interested {
  color: #7c3aed;
  background-color: #f5f3ff;
  border-color: #ddd6fe;
}

.status-paid {
  color: #16a34a;
  background-color: #f0fdf4;
  border-color: #bbf7d0;
}

.status-lost {
  color: #64748b;
  background-color: #f8fafc;
  border-color: #e2e8f0;
}
</style>
