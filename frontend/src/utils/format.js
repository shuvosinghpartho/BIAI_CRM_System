export function formatDate(dateStr) {
  if (!dateStr) return 'N/A'
  try {
    const d = new Date(dateStr)
    return new Intl.DateTimeFormat('en-GB', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    }).format(d)
  } catch (e) {
    return dateStr
  }
}

export function formatTimeAgo(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diffHours = Math.floor((now - d) / (1000 * 60 * 60))
  
  if (diffHours < 1) return 'Just now'
  if (diffHours < 24) return `${diffHours}h ago`
  const days = Math.floor(diffHours / 24)
  return `${days}d ago`
}

export function capitalize(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export function getChannelBadgeClass(channel) {
  const map = {
    whatsapp: 'badge-whatsapp',
    facebook: 'badge-facebook',
    website: 'badge-website',
    phone: 'badge-phone'
  }
  return map[channel?.toLowerCase()] || 'badge-unknown'
}

export function getInterestBadgeClass(interest) {
  const map = {
    bootcamp: 'badge-bootcamp',
    fellowship: 'badge-fellowship',
    corporate: 'badge-corporate',
    unknown: 'badge-unknown'
  }
  return map[interest?.toLowerCase()] || 'badge-unknown'
}
