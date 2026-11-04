<template>
  <form class="enquiry-form" @submit.prevent="handleSubmit">
    <div class="form-grid">
      <!-- Name -->
      <div class="form-group">
        <label for="name">Sender Name</label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          placeholder="e.g. Rafi Ahmed"
          class="form-control"
        />
      </div>

      <!-- Phone -->
      <div class="form-group">
        <label for="phone">Phone Number (01XXXXXXXXX)</label>
        <input
          id="phone"
          v-model="form.phone"
          type="text"
          placeholder="e.g. 01711000001"
          class="form-control font-mono"
        />
      </div>

      <!-- Channel Source -->
      <div class="form-group">
        <label for="source">Channel / Source *</label>
        <select id="source" v-model="form.source" required class="form-control">
          <option value="whatsapp">WhatsApp</option>
          <option value="facebook">Facebook</option>
          <option value="website">Website</option>
          <option value="phone">Phone Call</option>
        </select>
      </div>

      <!-- Interest -->
      <div class="form-group">
        <label for="interest">Program Interest</label>
        <select id="interest" v-model="form.interest" class="form-control">
          <option value="bootcamp">Bootcamp (3-day)</option>
          <option value="fellowship">Fellowship (6-month)</option>
          <option value="corporate">Corporate Training</option>
          <option value="unknown">Unknown / General</option>
        </select>
      </div>

      <!-- Enquiry Type -->
      <div class="form-group">
        <label for="enquiry_type">Enquiry Classification *</label>
        <select id="enquiry_type" v-model="form.enquiry_type" required class="form-control">
          <option value="sales">Sales (Goes to Pipeline)</option>
          <option value="support">Support Issue</option>
          <option value="job_seeker">Job Seeker</option>
          <option value="spam">Spam</option>
        </select>
      </div>

      <!-- Language -->
      <div class="form-group">
        <label for="language">Detected Language</label>
        <select id="language" v-model="form.language" class="form-control">
          <option value="banglish">Banglish</option>
          <option value="bangla">Bangla</option>
          <option value="english">English</option>
        </select>
      </div>
    </div>

    <!-- Message Body -->
    <div class="form-group full-width">
      <label for="message">Enquiry Message *</label>
      <textarea
        id="message"
        v-model="form.message"
        rows="4"
        required
        placeholder="Paste full customer message here..."
        class="form-control"
      ></textarea>
    </div>

    <!-- Submit buttons -->
    <div class="form-actions">
      <button
        type="submit"
        :disabled="saving"
        class="btn-primary"
      >
        <svg v-if="!saving" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
          <polyline points="17 21 17 13 7 13 7 21"/>
          <polyline points="7 3 7 8 15 8"/>
        </svg>
        <span>{{ saving ? 'Saving to CRM...' : 'Save Enquiry' }}</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({})
  },
  saving: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['save'])

const form = reactive({
  name: props.initialData.name || '',
  phone: props.initialData.phone || '',
  source: props.initialData.source || 'website',
  interest: props.initialData.interest || 'unknown',
  enquiry_type: props.initialData.enquiry_type || 'sales',
  language: props.initialData.language || 'english',
  message: props.initialData.message || ''
})

watch(() => props.initialData, (newVal) => {
  if (newVal) {
    form.name = newVal.name || ''
    form.phone = newVal.phone || ''
    form.source = newVal.source || 'website'
    form.interest = newVal.interest || 'unknown'
    form.enquiry_type = newVal.enquiry_type || 'sales'
    form.language = newVal.language || 'english'
    form.message = newVal.message || form.message
  }
}, { deep: true })

function handleSubmit() {
  emit('save', { ...form })
}
</script>

<style scoped>
.enquiry-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.form-control {
  padding: 0.65rem 0.85rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background-color: #ffffff;
  color: var(--text-main);
  transition: border-color 0.15s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.font-mono {
  font-family: var(--font-mono);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 0.75rem;
}
</style>
