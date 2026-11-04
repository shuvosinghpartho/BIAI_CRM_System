/**
 * Dynamic Favicon and Page Title Manager for BIAI CRM
 * Generates high-res inline SVG icons matching route and overdue notification states.
 */

export function setDynamicFavicon(routePath, overdueCount = 0) {
  let svgIcon = ''

  if (routePath.includes('summary')) {
    // Analytics Bar Chart Icon (Crimson/Violet)
    svgIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
      <rect width="32" height="32" rx="8" fill="#0f172a"/>
      <path d="M8 24V16M14 24V10M20 24V14M26 24V6" stroke="#f43f5e" stroke-width="3" stroke-linecap="round"/>
      ${overdueCount > 0 ? '<circle cx="25" cy="7" r="4.5" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>' : ''}
    </svg>`
  } else if (routePath.includes('other')) {
    // Inbox / Archive Icon (Amber)
    svgIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
      <rect width="32" height="32" rx="8" fill="#0f172a"/>
      <rect x="6" y="8" width="20" height="16" rx="3" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
      <path d="M6 15h6a4 4 0 0 0 8 0h6" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
    </svg>`
  } else if (routePath.includes('add')) {
    // Sparkle / Add Lead Icon (Emerald)
    svgIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
      <rect width="32" height="32" rx="8" fill="#0f172a"/>
      <circle cx="16" cy="16" r="11" fill="none" stroke="#10b981" stroke-width="2.5"/>
      <line x1="16" y1="10" x2="16" y2="22" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="10" y1="16" x2="22" y2="16" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`
  } else {
    // Pipeline Kanban Board Icon (Default / Blue-Violet)
    svgIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
      <rect width="32" height="32" rx="8" fill="#090d16"/>
      <rect x="6" y="8" width="5" height="16" rx="2" fill="#6366f1"/>
      <rect x="13.5" y="8" width="5" height="11" rx="2" fill="#38bdf8"/>
      <rect x="21" y="8" width="5" height="14" rx="2" fill="#10b981"/>
      ${overdueCount > 0 ? '<circle cx="26" cy="6" r="4.5" fill="#e11d48" stroke="#ffffff" stroke-width="1.5"/>' : ''}
    </svg>`
  }

  const svgDataUrl = `data:image/svg+xml;utf8,${encodeURIComponent(svgIcon.trim())}`
  
  let link = document.querySelector("link[rel*='icon']")
  if (!link) {
    link = document.createElement('link')
    link.type = 'image/svg+xml'
    link.rel = 'icon'
    document.getElementsByTagName('head')[0].appendChild(link)
  }
  link.href = svgDataUrl
}

export function updatePageMeta(routeName, extraInfo = {}) {
  const overdue = extraInfo.overdueCount || 0
  const salesCount = extraInfo.salesCount || 0
  let title = 'BIAI CRM • Bangladesh AI Institute'

  switch (routeName) {
    case 'pipeline':
      title = overdue > 0 
        ? `🚨 (${overdue} Overdue) Pipeline • BIAI CRM`
        : `Pipeline (${salesCount} Leads) • BIAI CRM`
      break
    case 'add-enquiry':
      title = `+ New Lead Auto-fill • BIAI CRM`
      break
    case 'other-enquiries':
      title = `Non-Sales (${extraInfo.otherCount || 0}) • BIAI CRM`
      break
    case 'summary':
      title = `Executive Summary • BIAI CRM`
      break
  }

  document.title = title
}
