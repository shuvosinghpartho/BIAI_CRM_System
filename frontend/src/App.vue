<template>
  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-badge">
          <span>B</span>
        </div>
        <div>
          <div class="brand-title">BIAI<span class="brand-tag">CRM</span></div>
          <div class="brand-subtitle">Admissions & Pipeline Intelligence</div>
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
        <div class="engine-status">
          <span class="pulse-dot"></span>
          <span>AI Engine Online</span>
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

        <div class="top-bar-right">
          <!-- Theme Toggle Switcher -->
          <button
            type="button"
            class="theme-toggle-btn"
            @click="store.toggleTheme"
          >
            <template v-if="store.theme === 'dark'">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="4"/>
                <path d="M12 2v2"/>
                <path d="M12 20v2"/>
                <path d="m4.93 4.93 1.41 1.41"/>
                <path d="m17.66 17.66 1.41 1.41"/>
                <path d="M2 12h2"/>
                <path d="M20 12h2"/>
                <path d="m6.34 17.66-1.41 1.41"/>
                <path d="m19.07 4.93-1.41 1.41"/>
              </svg>
              <span>Dark Theme</span>
            </template>
            <template v-else>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#e11d48" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
              </svg>
              <span>Light Theme</span>
            </template>
          </button>

          <div class="top-bar-stats">
            <div class="stat-chip">
              <span>Sales Leads:</span>
              <strong>{{ store.salesEnquiries.length }}</strong>
            </div>
            <div v-if="overdueCount > 0" class="stat-chip overdue">
              <span>Overdue:</span>
              <strong>{{ overdueCount }}</strong>
            </div>
          </div>
        </div>
      </header>

      <main class="page-body">
        <RouterView />
      </main>
    </div>

    <!-- Floating Global Toasts -->
    <div class="toast-container">
      <div
        v-for="t in store.toasts"
        :key="t.id"
        class="toast"
        :class="`toast-${t.type}`"
        @click="store.removeToast(t.id)"
      >
        <span>{{ t.message }}</span>
      </div>
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
    case 'pipeline': return 'Track and transition qualified sales leads from enquiry to enrollment.'
    case 'add-enquiry': return 'Paste any message to extract CRM fields and draft tailored replies.'
    case 'other-enquiries': return 'Review support requests, job seeker applications, and spam.'
    case 'summary': return 'Executive AI report of weekly performance and leads requiring follow-up.'
    default: return 'Bangladesh AI Institute customer relationship management system.'
  }
})

onMounted(() => {
  store.initTheme()
  store.fetchAll()
})
</script>

<style scoped>
.page-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
