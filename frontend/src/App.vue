<template>
  <div class="app-container">
    <!-- Top Cyber Route Progress Bar (Active when switching pages) -->
    <div class="route-progress-container" :class="{ active: isNavigating }">
      <div class="route-progress-bar">
        <div class="progress-glow-head"></div>
      </div>
    </div>

    <!-- Initial App Splash Preloader (When loading the site) -->
    <Transition name="splash-fade">
      <div v-if="isAppInitializing" class="app-splash-preloader">
        <div class="splash-card">
          <div class="splash-logo-container">
            <div class="splash-logo-orb">
              <span>B</span>
            </div>
            <div class="splash-pulse-ring ring-1"></div>
            <div class="splash-pulse-ring ring-2"></div>
          </div>
          
          <div class="splash-branding">
            <h2 class="splash-title">BIAI<span class="splash-tag">CRM</span></h2>
            <p class="splash-subtitle">Admissions & Pipeline Intelligence System</p>
          </div>

          <div class="splash-progress-track">
            <div class="splash-progress-fill">
              <div class="splash-streak"></div>
            </div>
          </div>

          <div class="splash-status-text">
            <span class="splash-pulse-dot"></span>
            <span>Initializing Workspace & AI Engine...</span>
          </div>
        </div>
      </div>
    </Transition>

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

      <!-- Smooth Page Transition Area -->
      <main class="page-body">
        <RouterView v-slot="{ Component, route: currentRoute }">
          <Transition name="page-fade-slide" mode="out-in">
            <component :is="Component" :key="currentRoute.path" />
          </Transition>
        </RouterView>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, RouterLink, RouterView } from 'vue-router'
import { useEnquiriesStore } from './stores/enquiries'
import { isNavigating } from './router/index'
import { setDynamicFavicon, updatePageMeta } from './utils/dynamicFavicon'

const route = useRoute()
const store = useEnquiriesStore()

const isAppInitializing = ref(true)

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

onMounted(async () => {
  store.initTheme()
  try {
    await store.fetchAll()
  } finally {
    // Smooth reveal after initial workspace load
    setTimeout(() => {
      isAppInitializing.value = false
    }, 650)
  }
})
</script>

<style scoped>
/* ==========================================================================
   TOP CYBER ROUTE PROGRESS BAR (When switching pages)
   ========================================================================== */
.route-progress-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  z-index: 999999;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.route-progress-container.active {
  opacity: 1;
}

.route-progress-bar {
  height: 100%;
  width: 100%;
  background: linear-gradient(90deg, #e11d48, #a855f7, #38bdf8);
  box-shadow: 0 0 12px #e11d48, 0 0 20px #a855f7;
  position: relative;
  animation: routeLoad 0.4s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
}

.progress-glow-head {
  position: absolute;
  right: 0;
  top: -2px;
  width: 20px;
  height: 7px;
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 0 14px #ffffff, 0 0 24px #38bdf8;
}

@keyframes routeLoad {
  0% { transform: scaleX(0); transform-origin: left; }
  60% { transform: scaleX(0.75); transform-origin: left; }
  100% { transform: scaleX(1); transform-origin: left; }
}

/* ==========================================================================
   SMOOTH PAGE TRANSITIONS (Between routes)
   ========================================================================== */
.page-fade-slide-enter-active,
.page-fade-slide-leave-active {
  transition: opacity 0.24s cubic-bezier(0.16, 1, 0.3, 1), transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
}

.page-fade-slide-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.995);
}

.page-fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.995);
}

/* ==========================================================================
   INITIAL APP SPLASH PRELOADER (When site loads)
   ========================================================================== */
.app-splash-preloader {
  position: fixed;
  inset: 0;
  background: var(--bg-app);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999998;
}

.splash-fade-enter-active,
.splash-fade-leave-active {
  transition: opacity 0.45s ease-out, transform 0.45s ease-out;
}

.splash-fade-enter-from,
.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.03);
}

.splash-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1.25rem;
  padding: 2.5rem 3rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg), 0 0 40px var(--primary-glow);
  max-width: 440px;
  width: 90%;
}

.splash-logo-container {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.splash-logo-orb {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-hover));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.6rem;
  box-shadow: 0 0 25px var(--primary-glow);
  z-index: 2;
}

.splash-pulse-ring {
  position: absolute;
  border-radius: 22px;
  border: 2px solid var(--primary);
  pointer-events: none;
  animation: splashRipple 2s cubic-bezier(0.1, 0.8, 0.3, 1) infinite;
}

.ring-1 {
  width: 72px;
  height: 72px;
}

.ring-2 {
  width: 88px;
  height: 88px;
  animation-delay: 1s;
}

@keyframes splashRipple {
  0% { transform: scale(0.9); opacity: 0.8; }
  100% { transform: scale(1.4); opacity: 0; }
}

.splash-branding {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.splash-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.splash-tag {
  color: var(--primary);
  font-size: 0.85rem;
  background: var(--primary-light);
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  margin-left: 0.4rem;
}

.splash-subtitle {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}

.splash-progress-track {
  width: 100%;
  height: 5px;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-color);
  border-radius: 9999px;
  overflow: hidden;
  position: relative;
}

.splash-progress-fill {
  height: 100%;
  width: 100%;
  background: linear-gradient(90deg, #e11d48, #a855f7, #38bdf8);
  border-radius: 9999px;
  position: relative;
  animation: splashProgressSweep 1.2s ease-in-out infinite alternate;
}

.splash-streak {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.7), transparent);
  animation: streakMove 1.4s infinite;
}

@keyframes splashProgressSweep {
  0% { width: 30%; }
  100% { width: 95%; }
}

@keyframes streakMove {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.splash-status-text {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
}

.splash-pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: 0 0 8px var(--primary);
  animation: pulse-dot-anim 1.5s infinite;
}

/* ==========================================================================
   PAGE LAYOUT
   ========================================================================== */
.page-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  overflow: hidden;
  position: relative;
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
