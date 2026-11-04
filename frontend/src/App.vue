<template>
  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-icon">B</div>
        <div>
          <div class="brand-title">BIAI CRM</div>
          <div class="brand-subtitle">Bangladesh AI Institute</div>
        </div>
      </div>

      <ul class="nav-links">
        <li class="nav-item">
          <RouterLink to="/">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2"/>
              <path d="M3 9h18"/>
              <path d="M9 21V9"/>
            </svg>
            Pipeline Board
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/add">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 5v14"/>
              <path d="M5 12h14"/>
            </svg>
            Add Enquiry
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/other">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="20" height="16" x="2" y="4" rx="2"/>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
            Other Enquiries
            <span v-if="otherCount > 0" class="nav-badge">{{ otherCount }}</span>
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/summary">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18"/>
              <path d="m19 9-5 5-4-4-3 3"/>
            </svg>
            Weekly Summary
            <span v-if="overdueCount > 0" class="nav-badge danger">{{ overdueCount }}</span>
          </RouterLink>
        </li>
      </ul>

      <div class="sidebar-footer">
        <div class="ai-status-indicator">
          <span class="pulse-dot"></span>
          <span>Gemini AI Connected</span>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-content">
      <header class="top-bar">
        <div>
          <h1 class="page-title">{{ currentRouteTitle }}</h1>
          <p class="page-description">{{ currentRouteDesc }}</p>
        </div>

        <div class="top-bar-stats">
          <div class="stat-pill">
            <span>Sales Leads:</span>
            <strong>{{ store.salesEnquiries.length }}</strong>
          </div>
          <div v-if="overdueCount > 0" class="stat-pill overdue">
            <span>Overdue:</span>
            <strong>{{ overdueCount }}</strong>
          </div>
        </div>
      </header>

      <main class="page-body">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, RouterLink, RouterView } from 'vue-router'
import { useEnquiriesStore } from './stores/enquiries'

const route = useRoute()
const store = useEnquiriesStore()

const otherCount = computed(() => store.otherEnquiries.length)
const overdueCount = computed(() => store.overdueCount)

const currentRouteTitle = computed(() => {
  switch (route.name) {
    case 'pipeline': return 'Sales Enquiry Pipeline'
    case 'add-enquiry': return 'New Enquiry & AI Extraction'
    case 'other-enquiries': return 'Non-Sales Enquiries'
    case 'summary': return 'Weekly Summary & Overdue Reports'
    default: return 'BIAI Admissions CRM'
  }
})

const currentRouteDesc = computed(() => {
  switch (route.name) {
    case 'pipeline': return 'Track and transition sales leads from initial enquiry to enrollment.'
    case 'add-enquiry': return 'Paste any message to extract CRM fields and draft tailored replies.'
    case 'other-enquiries': return 'Review support requests, job seeker applications, and spam.'
    case 'summary': return 'Executive AI report of weekly performance and leads requiring follow-up.'
    default: return 'Bangladesh AI Institute customer relationship management system.'
  }
})

onMounted(() => {
  store.fetchAll()
})
</script>

<style scoped>
.sidebar-footer {
  padding: 1.25rem;
  border-top: 1px solid #1e293b;
  font-size: 0.775rem;
}

.ai-status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.top-bar-stats {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stat-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background-color: #f1f5f9;
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  color: #475569;
}

.stat-pill strong {
  color: #0f172a;
}

.stat-pill.overdue {
  background-color: #fee2e2;
  color: #b91c1c;
}

.stat-pill.overdue strong {
  color: #991b1b;
}

.page-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
