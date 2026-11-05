<template>
  <div
    class="enquiry-card card-box"
    :class="{ 'is-overdue': overdue }"
    @click="openModal"
  >
    <!-- Left Flush Overdue Glow Strip -->
    <div v-if="overdue" class="overdue-accent-strip"></div>

    <!-- Row 1: Prospect Profile (Avatar, Name, Phone) & Overdue Badge -->
    <div class="card-row-top">
      <div class="prospect-header">
        <div class="avatar-ring" :class="`channel-${(enquiry.source || '').toLowerCase()}`">
          <span class="avatar-letter">{{ (enquiry.name ? enquiry.name[0] : 'P').toUpperCase() }}</span>
          <span class="channel-dot" :title="`Source: ${enquiry.source}`">
            <!-- WhatsApp -->
            <svg v-if="enquiry.source === 'whatsapp'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.301-.15-1.78-.879-2.056-.98-.276-.1-.477-.15-.678.15-.2.301-.778.98-.954 1.18-.176.2-.352.226-.653.076-.301-.15-1.272-.469-2.423-1.496-.896-.799-1.501-1.786-1.677-2.087-.176-.301-.019-.464.132-.614.136-.135.301-.352.452-.528.15-.176.2-.301.301-.502.101-.201.05-.377-.025-.528-.075-.15-.678-1.634-.929-2.237-.245-.588-.493-.508-.678-.517-.176-.009-.377-.009-.578-.009s-.528.075-.804.377c-.276.301-1.055 1.03-1.055 2.512s1.08 2.914 1.231 3.115c.15.201 2.125 3.245 5.148 4.551.719.311 1.281.497 1.719.636.723.23 1.381.197 1.901.12.58-.087 1.78-.727 2.031-1.43.251-.703.251-1.306.176-1.43-.075-.125-.276-.201-.577-.351zM12.04 2C6.516 2 2.028 6.488 2.028 12.012c0 1.94.556 3.754 1.517 5.29L2 22l4.823-1.495c1.488.887 3.224 1.395 5.08 1.395 5.524 0 10.012-4.488 10.012-10.012S17.564 2 12.04 2z"/>
            </svg>
            <!-- Facebook -->
            <svg v-else-if="enquiry.source === 'facebook'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
            </svg>
            <!-- Website -->
            <svg v-else-if="enquiry.source === 'website'" xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            <!-- Phone -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
            </svg>
          </span>
        </div>

        <div class="prospect-info">
          <h4 class="prospect-name" :title="enquiry.name || 'Anonymous Prospect'">
            {{ enquiry.name || 'Anonymous Prospect' }}
          </h4>
          <span v-if="enquiry.phone" class="prospect-phone font-mono">
            {{ enquiry.phone }}
          </span>
          <span v-else class="prospect-phone-empty">No phone recorded</span>
        </div>
      </div>

      <!-- Overdue Badge (Separated in Top-Right Corner) -->
      <div v-if="overdue" class="top-status-badge">
        <OverdueBadge :overdue="overdue" />
      </div>
    </div>

    <!-- Row 2: Metadata Tags & Quick Contact Actions -->
    <div class="card-row-meta">
      <div class="tags-cluster">
        <!-- Track Tag -->
        <span class="track-tag" :class="`track-${(enquiry.interest || 'unknown').toLowerCase()}`">
          <span v-if="enquiry.interest === 'bootcamp'">⚡ Bootcamp</span>
          <span v-else-if="enquiry.interest === 'fellowship'">🎓 Fellowship</span>
          <span v-else-if="enquiry.interest === 'corporate'">🏢 Corporate</span>
          <span v-else>📌 General</span>
        </span>

        <!-- Language Tag -->
        <span v-if="enquiry.language" class="lang-tag">
          <span v-if="enquiry.language === 'bangla'">🇧🇩 বাংলা</span>
          <span v-else-if="enquiry.language === 'banglish'">🗣️ Banglish</span>
          <span v-else>🌐 English</span>
        </span>

        <!-- AI Draft Ready -->
        <span v-if="enquiry.ai_reply" class="ai-ready-tag" title="AI reply draft prepared">
          ✨ AI Ready
        </span>
      </div>

      <!-- Fast Action Triggers (WhatsApp & Phone) -->
      <div class="card-quick-actions" @click.stop>
        <!-- WhatsApp Direct -->
        <a
          v-if="whatsAppUrl"
          :href="whatsAppUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="card-action-btn wa-btn"
          title="Open WhatsApp chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.301-.15-1.78-.879-2.056-.98-.276-.1-.477-.15-.678.15-.2.301-.778.98-.954 1.18-.176.2-.352.226-.653.076-.301-.15-1.272-.469-2.423-1.496-.896-.799-1.501-1.786-1.677-2.087-.176-.301-.019-.464.132-.614.136-.135.301-.352.452-.528.15-.176.2-.301.301-.502.101-.201.05-.377-.025-.528-.075-.15-.678-1.634-.929-2.237-.245-.588-.493-.508-.678-.517-.176-.009-.377-.009-.578-.009s-.528.075-.804.377c-.276.301-1.055 1.03-1.055 2.512s1.08 2.914 1.231 3.115c.15.201 2.125 3.245 5.148 4.551.719.311 1.281.497 1.719.636.723.23 1.381.197 1.901.12.58-.087 1.78-.727 2.031-1.43.251-.703.251-1.306.176-1.43-.075-.125-.276-.201-.577-.351zM12.04 2C6.516 2 2.028 6.488 2.028 12.012c0 1.94.556 3.754 1.517 5.29L2 22l4.823-1.495c1.488.887 3.224 1.395 5.08 1.395 5.524 0 10.012-4.488 10.012-10.012S17.564 2 12.04 2z"/>
          </svg>
        </a>

        <!-- Phone Call -->
        <a
          v-if="telUrl"
          :href="telUrl"
          class="card-action-btn call-btn"
          title="Direct Phone Call"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
          </svg>
        </a>
      </div>
    </div>

    <!-- Row 3: Message Excerpt Bubble -->
    <div class="message-preview-box">
      <div class="quote-mark">“</div>
      <p class="message-preview-text">{{ enquiry.message }}</p>
    </div>

    <!-- Row 4: Card Footer (Time & Stage Selector) -->
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
import { formatTimeAgo, formatWhatsAppUrl, formatTelUrl } from '../utils/format'

const props = defineProps({
  enquiry: {
    type: Object,
    required: true
  }
})

const store = useEnquiriesStore()
const overdue = computed(() => store.isOverdue(props.enquiry))

const whatsAppUrl = computed(() => formatWhatsAppUrl(props.enquiry?.phone))
const telUrl = computed(() => formatTelUrl(props.enquiry?.phone))

async function handleStatusChange(newStatus) {
  if (props.enquiry.status === newStatus) return
  await store.updateStatus(props.enquiry.id, newStatus)
}

function openModal() {
  store.openDetailModal(props.enquiry)
}
</script>

<style scoped>
.enquiry-card {
  padding: 0.85rem 0.95rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  cursor: pointer;
  border-radius: var(--radius-md);
  position: relative;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
  overflow: hidden;
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
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, var(--card-bg) 100%);
  border-color: rgba(239, 68, 68, 0.35);
}

/* Flush Overdue Accent Strip (No border clash) */
.overdue-accent-strip {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3.5px;
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}

/* ==========================================================================
   ROW 1: PROSPECT HEADER & TOP-RIGHT STATUS BADGE
   ========================================================================== */
.card-row-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  min-height: 36px;
}

.prospect-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex: 1;
  min-width: 0;
}

.avatar-ring {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--bg-surface-elevated), var(--border-color));
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-letter {
  font-size: 0.82rem;
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
  border: 1.5px solid var(--card-bg);
}

.channel-whatsapp .channel-dot { background: #22c55e; }
.channel-facebook .channel-dot { background: #3b82f6; }
.channel-website .channel-dot { background: #06b6d4; }
.channel-phone .channel-dot { background: #a855f7; }

.prospect-info {
  display: flex;
  flex-direction: column;
  gap: 0.08rem;
  flex: 1;
  min-width: 0;
}

.prospect-name {
  font-size: 0.865rem;
  font-weight: 800;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

.prospect-phone {
  font-size: 0.71rem;
  color: var(--text-muted);
  font-weight: 600;
  line-height: 1.15;
}

.prospect-phone-empty {
  font-size: 0.68rem;
  color: var(--text-muted);
  font-style: italic;
  opacity: 0.7;
}

/* Dedicated Top-Right Status Badge (Zero Overlap) */
.top-status-badge {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  margin-top: 1px;
}

/* ==========================================================================
   ROW 2: METADATA TAGS & FAST CONTACT ACTIONS
   ========================================================================== */
.card-row-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.tags-cluster {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.3rem;
  flex: 1;
  min-width: 0;
}

.track-tag {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.12rem 0.45rem;
  border-radius: var(--radius-full);
  border: 1px solid transparent;
  white-space: nowrap;
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
  font-size: 0.66rem;
  font-weight: 700;
  padding: 0.12rem 0.42rem;
  border-radius: var(--radius-full);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  white-space: nowrap;
}

.ai-ready-tag {
  font-size: 0.64rem;
  font-weight: 800;
  padding: 0.1rem 0.4rem;
  border-radius: var(--radius-full);
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

/* Quick Action Triggers (WhatsApp & Phone) */
.card-quick-actions {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  flex-shrink: 0;
}

.card-action-btn {
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
  cursor: pointer;
}

.card-action-btn.wa-btn:hover {
  background: #22c55e;
  border-color: #22c55e;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
  transform: scale(1.08);
}

.card-action-btn.call-btn:hover {
  background: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
  transform: scale(1.08);
}

/* ==========================================================================
   ROW 3: MESSAGE PREVIEW
   ========================================================================== */
.message-preview-box {
  position: relative;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.65rem 0.5rem 1.15rem;
}

.quote-mark {
  position: absolute;
  top: -2px;
  left: 0.3rem;
  font-size: 1.05rem;
  font-family: Georgia, serif;
  color: var(--primary);
  opacity: 0.65;
  line-height: 1;
}

.message-preview-text {
  font-size: 0.765rem;
  color: var(--text-main);
  line-height: 1.38;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-style: italic;
  opacity: 0.9;
}

/* ==========================================================================
   ROW 4: FOOTER (TIME & STAGE SELECTOR)
   ========================================================================== */
.card-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.35rem;
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
