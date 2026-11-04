<template>
  <div class="reply-box-card">
    <div class="reply-box-header">
      <div class="header-left">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sparkle-icon">
          <path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/>
        </svg>
        <span class="title">Suggested AI Response</span>
        <span v-if="language" class="lang-pill">{{ language.toUpperCase() }}</span>
      </div>
      <div class="header-actions">
        <button
          v-if="replyText"
          type="button"
          class="btn-copy"
          :class="{ copied: isCopied }"
          @click="copyReply"
        >
          <svg v-if="!isCopied" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
            <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          {{ isCopied ? 'Copied!' : 'Copy Reply' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="reply-loading">
      <div class="reply-loading-top">
        <div class="spinner-sm"></div>
        <span>Synthesizing tailored AI response...</span>
      </div>
      <div class="skeleton-lines">
        <div class="skeleton-line full skeleton-pulse"></div>
        <div class="skeleton-line md skeleton-pulse"></div>
      </div>
    </div>

    <div v-else-if="replyText" class="reply-body">
      <textarea
        v-model="editableReply"
        rows="4"
        class="reply-textarea"
        placeholder="Edit response if needed before copying..."
      ></textarea>
    </div>

    <div v-else class="reply-empty">
      <p>No response generated yet. Click "Auto-fill with AI" or paste a message above.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'

const props = defineProps({
  replyText: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:replyText'])
const store = useEnquiriesStore()

const editableReply = ref(props.replyText)
const isCopied = ref(false)

watch(() => props.replyText, (newVal) => {
  editableReply.value = newVal
})

watch(editableReply, (val) => {
  emit('update:replyText', val)
})

async function copyReply() {
  if (!editableReply.value) return
  try {
    await navigator.clipboard.writeText(editableReply.value)
    isCopied.value = true
    store.showToast('Suggested reply copied to clipboard!', 'success')
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
  } catch (err) {
    const textArea = document.createElement("textarea")
    textArea.value = editableReply.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    isCopied.value = true
    store.showToast('Suggested reply copied!', 'success')
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
  }
}
</script>

<style scoped>
.reply-box-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  margin-top: 1.25rem;
}

.reply-box-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sparkle-icon {
  color: var(--primary);
}

.title {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-main);
}

.lang-pill {
  font-size: 0.675rem;
  font-weight: 700;
  background: var(--primary-light);
  color: var(--primary);
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  letter-spacing: 0.05em;
}

.btn-copy {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.85rem;
  background-color: var(--primary);
  color: #ffffff;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.15s ease;
}

.btn-copy:hover {
  background-color: var(--primary-hover);
}

.btn-copy.copied {
  background-color: var(--success);
}

.reply-loading {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem;
  color: var(--text-muted);
  font-size: 0.85rem;
  background: var(--bg-surface-elevated);
  border-radius: var(--radius-sm);
}

.reply-loading-top {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-weight: 600;
  color: var(--text-main);
}

.skeleton-lines {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
}

.reply-body {
  width: 100%;
}

.reply-textarea {
  width: 100%;
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--input-border);
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-main);
  resize: vertical;
  background-color: var(--input-bg);
}

.reply-textarea:focus {
  outline: none;
  border-color: var(--primary);
}

.reply-empty {
  color: var(--text-muted);
  font-size: 0.85rem;
  font-style: italic;
  padding: 0.5rem 0;
}
</style>
