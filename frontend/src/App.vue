<template>
  <div class="app-container">
    <!-- Desktop Sidebar Navigation -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-badge">
          <span>B</span>
        </div>
        <div>
          <div class="brand-title">BIAI<span class="brand-tag">CRM</span></div>
          <div class="brand-subtitle">Admissions & Lead Intelligence</div>
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
            <span>Pipeline Board</span>
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/add">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            <span>Add Enquiry</span>
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/other">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="20" height="16" x="2" y="4" rx="2"/>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
            <span>Other Enquiries</span>
            <span v-if="otherCount > 0" class="nav-badge">{{ otherCount }}</span>
          </RouterLink>
        </li>

        <li class="nav-item">
          <RouterLink to="/summary">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18"/>
              <path d="m19 9-5 5-4-4-3 3"/>
            </svg>
            <span>Weekly Summary</span>
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
        <div class="top-bar-left">
          <div class="mobile-brand-pill">
            <div class="logo-badge mini"><span>B</span></div>
            <strong>BIAI CRM</strong>
          </div>
          <div>
            <h1 class="page-title">{{ currentRouteTitle }}</h1>
            <p class="page-description">{{ currentRouteDesc }}</p>
          </div>
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
              <span>Leads:</span>
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

    <!-- Mobile Bottom Navigation Dock -->
    <nav class="mobile-bottom-dock">
      <RouterLink to="/" class="dock-item" :class="{ active: route.name === 'pipeline' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="18" x="3" y="3" rx="2"/>
          <path d="M3 9h18"/>
          <path d="M9 21V9"/>
        </svg>
        <span>Pipeline</span>
      </RouterLink>

      <RouterLink to="/add" class="dock-item" :class="{ active: route.name === 'add-enquiry' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="16"/>
          <line x1="8" y1="12" x2="16" y2="12"/>
        </svg>
        <span>Add Lead</span>
      </RouterLink>

      <RouterLink to="/other" class="dock-item" :class="{ active: route.name === 'other-enquiries' }">
        <div class="dock-icon-wrap">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="20" height="16" x="2" y="4" rx="2"/>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
          </svg>
          <span v-if="otherCount > 0" class="dock-badge">{{ otherCount }}</span>
        </div>
        <span>Other</span>
      </RouterLink>

      <RouterLink to="/summary" class="dock-item" :class="{ active: route.name === 'summary' }">
        <div class="dock-icon-wrap">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"/>
            <path d="m19 9-5 5-4-4-3 3"/>
          </svg>
          <span v-if="overdueCount > 0" class="dock-badge danger">{{ overdueCount }}</span>
        </div>
        <span>Summary</span>
      </RouterLink>
    </nav>

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
import { computed, onMounted, watch } from 'vue'
import { useRoute, RouterLink, RouterView } from 'vue-router'
import { useEnquiriesStore } from './stores/enquiries'
import { setDynamicFavicon, updatePageMeta } from './utils/dynamicFavicon'

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

// Dynamic Favicon and Page Meta Sync
watch(
  [() => route.path, () => store.overdueCount, () => store.salesEnquiries.length, () => store.otherEnquiries.length],
  () => {
    setDynamicFavicon(route.path, store.overdueCount)
    updatePageMeta(route.name, {
      overdueCount: store.overdueCount,
      salesCount: store.salesEnquiries.length,
      otherCount: store.otherEnquiries.length
    })
  },
  { immediate: true }
)

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

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-brand-pill {
  display: none;
  align-items: center;
  gap: 0.5rem;
}

.logo-badge.mini {
  width: 28px;
  height: 28px;
  font-size: 0.9rem;
}

/* Mobile Bottom Navigation Dock */
.mobile-bottom-dock {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--bg-surface);
  border-top: 1px solid var(--border-color);
  align-items: center;
  justify-content: space-around;
  z-index: 900;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.15);
}

.dock-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.7rem;
  font-weight: 700;
  transition: all 0.15s;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-sm);
}

.dock-item.active {
  color: var(--primary);
}

.dock-icon-wrap {
  position: relative;
  display: inline-flex;
}

.dock-badge {
  position: absolute;
  top: -4px;
  right: -8px;
  background: var(--primary);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 0.1rem 0.35rem;
  border-radius: 9999px;
  line-height: 1;
}

.dock-badge.danger {
  background: var(--danger);
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .mobile-brand-pill {
    display: flex;
  }

  .mobile-bottom-dock {
    display: flex;
  }

  .main-content {
    padding-bottom: 65px;
  }

  .page-description {
    display: none;
  }

  .page-title {
    font-size: 1.1rem;
  }
}
</style>
