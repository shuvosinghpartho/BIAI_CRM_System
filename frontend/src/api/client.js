import axios from 'axios'

const api = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json'
  }
})

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
  getWeeklySummary() {
    return api.get('/api/reports/weekly-summary')
  }
}
