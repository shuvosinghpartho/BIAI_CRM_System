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

/**
 * Builds a valid WhatsApp click-to-chat URL or returns null if the phone is invalid.
 * Handles Bangla/local BD numbers (01XXXXXXXXX) and international formats (+880, etc.)
 */
export function formatWhatsAppUrl(phone) {
  if (!phone || typeof phone !== 'string') return null
  const digits = phone.replace(/\D/g, '')
  if (digits.length < 8 || digits.length > 15) return null
  if (digits.startsWith('880')) return `https://wa.me/${digits}`
  if (digits.startsWith('01') && digits.length === 11) return `https://wa.me/88${digits}`
  return `https://wa.me/${digits}`
}

/**
 * Builds a valid tel: protocol link for direct phone dialing or returns null.
 */
export function formatTelUrl(phone) {
  if (!phone || typeof phone !== 'string') return null
  const cleaned = phone.trim().replace(/[^\d+]/g, '')
  if (cleaned.length < 5) return null
  return `tel:${cleaned}`
}


