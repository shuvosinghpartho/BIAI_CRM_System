<template>
  <div
    class="enquiry-card card-box"
    :class="{ 'is-overdue': overdue }"
    @click="openModal"
  >
    <!-- Card Top Header -->
    <div class="card-header-row">
      <div class="prospect-profile">
        <div class="avatar-ring" :class="`channel-${(enquiry.source || '').toLowerCase()}`">
          <span class="avatar-letter">{{ (enquiry.name ? enquiry.name[0] : 'P').toUpperCase() }}</span>
          <span class="channel-dot" :title="`Channel: ${enquiry.source}`">
            <svg v-if="enquiry.source === 'whatsapp'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
            </svg>
            <svg v-else-if="enquiry.source === 'facebook'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
            <svg v-else-if="enquiry.source === 'website'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
            </svg>
          </span>
        </div>

        <div class="prospect-text">
          <h4 class="prospect-name" :title="enquiry.name">{{ enquiry.name || 'Anonymous Prospect' }}</h4>
          <span v-if="enquiry.phone" class="prospect-phone font-mono">
            {{ enquiry.phone }}
          </span>
          <span v-else class="prospect-phone-empty">No phone recorded</span>
        </div>
      </div>

      <!-- Quick Action Badges & Buttons -->
      <div class="header-actions" @click.stop>
        <OverdueBadge :overdue="overdue" />
        
        <!-- Quick 1-Click WhatsApp -->
        <a
          v-if="cleanPhone"
          :href="`https://wa.me/${cleanPhone}`"
          target="_blank"
          rel="noopener noreferrer"
          class="card-action-icon wa-icon"
          title="Direct WhatsApp Message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
          </svg>
        </a>

        <!-- Quick 1-Click Call -->
        <a
          v-if="enquiry.phone"
          :href="`tel:${enquiry.phone}`"
          class="card-action-icon call-icon"
          title="Direct Phone Call"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
          </svg>
        </a>
      </div>
    </div>

    <!-- Tags Row: Track, Language, Channel -->
    <div class="tags-row">
      <!-- Course Track Badge -->
      <span class="track-tag" :class="`track-${(enquiry.interest || 'unknown').toLowerCase()}`">
        <span v-if="enquiry.interest === 'bootcamp'">⚡ Bootcamp</span>
        <span v-else-if="enquiry.interest === 'fellowship'">🎓 Fellowship</span>
        <span v-else-if="enquiry.interest === 'corporate'">🏢 Corporate</span>
        <span v-else>📌 General</span>
      </span>

      <!-- Language Badge -->
      <span v-if="enquiry.language" class="lang-tag">
        <span v-if="enquiry.language === 'bangla'">🇧🇩 বাংলা</span>
        <span v-else-if="enquiry.language === 'banglish'">🗣️ Banglish</span>
        <span v-else>🌐 English</span>
      </span>

      <!-- AI Reply Indicator -->
      <span v-if="enquiry.ai_reply" class="ai-ready-tag" title="AI Suggested reply is prepared">
        ✨ AI Draft
      </span>
    </div>

    <!-- Message Excerpt Bubble -->
    <div class="message-preview-box">
      <div class="quote-mark">“</div>
      <p class="message-preview-text">{{ enquiry.message }}</p>
    </div>

    <!-- Card Footer: Time Ago & Quick Stage Mover -->
    <div class="card-footer-row" @click.stop>
      <div class="time-meta-wrap">
        <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        <span>{{ formatTimeAgo(enquiry.created_at) }}</span>
      </div>

      <div class="stage-select-box">
        <StatusSelect
          :model-value="enquiry.status"
          @change="handleStatusChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useEnquiriesStore } from '../stores/enquiries'
import StatusSelect from './StatusSelect.vue'
import OverdueBadge from './OverdueBadge.vue'
import { formatTimeAgo } from '../utils/format'

const props = defineProps({
  enquiry: {
    type: Object,
    required: true
  }
})

const store = useEnquiriesStore()
const overdue = computed(() => store.isOverdue(props.enquiry))

const cleanPhone = computed(() => {
  if (!props.enquiry?.phone) return ''
  const digits = props.enquiry.phone.replace(/\D/g, '')
  if (digits.startsWith('880')) return digits
  if (digits.startsWith('01')) return '88' + digits
  return digits
})

async function handleStatusChange(newStatus) {
  await store.updateStatus(props.enquiry.id, newStatus)
}

function openModal() {
  store.openDetailModal(props.enquiry)
}
</script>

<style scoped>
.enquiry-card {
  padding: 0.95rem 1.05rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  cursor: pointer;
  border-radius: var(--radius-md);
  position: relative;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}

.enquiry-card:hover {
  transform: translateY(-2px);
  border-color: var(--primary);
  box-shadow: 0 8px 20px -4px var(--primary-glow);
}

.enquiry-card:active {
  transform: translateY(0);
}

.enquiry-card.is-overdue {
  border-left: 3.5px solid var(--danger);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.06) 0%, var(--card-bg) 100%);
}

/* Header Row */
.card-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.prospect-profile {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  min-width: 0;
  flex: 1;
}

.avatar-ring {
  position: relative;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--bg-surface-elevated), var(--border-color));
  border: 1.5px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-letter {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--text-main);
}

.channel-dot {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  border: 1.5px solid var(--bg-surface);
}

.channel-whatsapp .channel-dot { background: #22c55e; }
.channel-facebook .channel-dot { background: #3b82f6; }
.channel-website .channel-dot { background: #06b6d4; }
.channel-phone .channel-dot { background: #a855f7; }

.prospect-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.prospect-name {
  font-size: 0.885rem;
  font-weight: 800;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.01em;
  line-height: 1.25;
}

.prospect-phone {
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 600;
}

.prospect-phone-empty {
  font-size: 0.7rem;
  color: var(--text-muted);
  font-style: italic;
  opacity: 0.7;
}

/* Actions in Header */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-shrink: 0;
}

.card-action-icon {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  transition: all 0.15s ease;
  text-decoration: none;
}

.card-action-icon.wa-icon:hover {
  background: #22c55e;
  border-color: #22c55e;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
}

.card-action-icon.call-icon:hover {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
}

/* Tags Row */
.tags-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.track-tag {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-full);
  border: 1px solid transparent;
}

.track-bootcamp {
  background: rgba(34, 197, 94, 0.12);
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.3);
}

.track-fellowship {
  background: rgba(168, 85, 247, 0.12);
  color: #a855f7;
  border-color: rgba(168, 85, 247, 0.3);
}

.track-corporate {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
}

.track-unknown {
  background: var(--bg-surface-elevated);
  color: var(--text-muted);
  border-color: var(--border-color);
}

.lang-tag {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-full);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
}

.ai-ready-tag {
  font-size: 0.66rem;
  font-weight: 800;
  padding: 0.12rem 0.45rem;
  border-radius: var(--radius-full);
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  display: inline-flex;
  align-items: center;
}

/* Message Preview Box */
.message-preview-box {
  position: relative;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 0.55rem 0.65rem 0.55rem 1.25rem;
}

.quote-mark {
  position: absolute;
  top: -2px;
  left: 0.35rem;
  font-size: 1.1rem;
  font-family: Georgia, serif;
  color: var(--primary);
  opacity: 0.7;
  line-height: 1;
}

.message-preview-text {
  font-size: 0.775rem;
  color: var(--text-main);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-style: italic;
  opacity: 0.9;
}

/* Card Footer */
.card-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.4rem;
  border-top: 1px solid var(--border-color);
  gap: 0.5rem;
}

.time-meta-wrap {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
}

.stage-select-box {
  display: inline-flex;
}
</style>
