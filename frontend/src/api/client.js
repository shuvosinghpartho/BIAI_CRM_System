import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 30000, // 30s timeout for AI requests
  headers: {
    'Content-Type': 'application/json'
  }
})

// Global response error handler
api.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = 'Network connection error. Please ensure the backend is running.'
    if (error.response?.data?.detail) {
      message = error.response.data.detail
    } else if (error.message) {
      message = error.message
    }
    console.error('[API Error]:', message)
    return Promise.reject(new Error(message))
  }
)

export default {
  // Enquiries CRUD
  getEnquiries(params = {}) {
    return api.get('/api/enquiries', { params })
  },
  getEnquiry(id) {
    return api.get(`/api/enquiries/${id}`)
  },
  createEnquiry(payload) {
    return api.post('/api/enquiries', payload)
  },
  updateEnquiry(id, payload) {
    return api.patch(`/api/enquiries/${id}`, payload)
  },
  deleteEnquiry(id) {
    return api.delete(`/api/enquiries/${id}`)
  },

  // AI Extraction & Replies
  extract(payload) {
    return api.post('/api/ai/extract', payload)
  },
  suggestReply(payload) {
    return api.post('/api/ai/suggest-reply', payload)
  },

  // Reports & Analytics
  getOverdue() {
    return api.get('/api/reports/overdue')
  },
  getWeeklySummary(refresh = false) {
    return api.get('/api/reports/weekly-summary', { params: { refresh } })
  }
}
