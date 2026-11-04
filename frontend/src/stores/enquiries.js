import { defineStore } from 'pinia'
import api from '../api/client'

export const useEnquiriesStore = defineStore('enquiries', {
  state: () => ({
    enquiries: [],
    overdueList: [],
    loading: false,
    error: null,
    searchQuery: '',
    selectedChannel: 'all',
  }),

  getters: {
    salesEnquiries: (state) => {
      return state.enquiries.filter(e => e.enquiry_type === 'sales')
    },
    
    otherEnquiries: (state) => {
      return state.enquiries.filter(e => e.enquiry_type !== 'sales')
    },

    filteredSalesEnquiries: (state) => {
      let list = state.enquiries.filter(e => e.enquiry_type === 'sales')
      
      if (state.selectedChannel !== 'all') {
        list = list.filter(e => e.source === state.selectedChannel)
      }

      if (state.searchQuery.trim()) {
        const query = state.searchQuery.toLowerCase()
        list = list.filter(e => 
          (e.name && e.name.toLowerCase().includes(query)) ||
          (e.phone && e.phone.includes(query)) ||
          (e.message && e.message.toLowerCase().includes(query))
        )
      }
      return list
    },

    pipelineColumns() {
      const statuses = ['New', 'Contacted', 'Interested', 'Paid', 'Lost']
      const groups = {
        'New': [],
        'Contacted': [],
        'Interested': [],
        'Paid': [],
        'Lost': []
      }

      this.filteredSalesEnquiries.forEach(e => {
        const s = e.status || 'New'
        if (groups[s]) {
          groups[s].push(e)
        } else {
          groups['New'].push(e)
        }
      })

      return groups
    },

    isOverdue: (state) => (enquiry) => {
      if (enquiry.enquiry_type !== 'sales' || ['Paid', 'Lost'].includes(enquiry.status)) {
        return false
      }
      return state.overdueList.some(o => o.id === enquiry.id)
    },

    overdueCount: (state) => state.overdueList.length
  },

  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const [enqRes, overdueRes] = await Promise.all([
          api.getEnquiries(),
          api.getOverdue()
        ])
        this.enquiries = enqRes.data
        this.overdueList = overdueRes.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
      } finally {
        this.loading = false
      }
    },

    async updateStatus(id, newStatus) {
      try {
        const res = await api.updateEnquiry(id, { status: newStatus })
        const idx = this.enquiries.findIndex(e => e.id === id)
        if (idx !== -1) {
          this.enquiries[idx] = res.data
        }
        // Refresh overdue list
        const overdueRes = await api.getOverdue()
        this.overdueList = overdueRes.data
        return res.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      }
    },

    async addEnquiry(payload) {
      this.loading = true
      try {
        const res = await api.createEnquiry(payload)
        this.enquiries.unshift(res.data)
        const overdueRes = await api.getOverdue()
        this.overdueList = overdueRes.data
        return res.data
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteEnquiry(id) {
      try {
        await api.deleteEnquiry(id)
        this.enquiries = this.enquiries.filter(e => e.id !== id)
        this.overdueList = this.overdueList.filter(e => e.id !== id)
      } catch (err) {
        this.error = err.response?.data?.detail || err.message
        throw err
      }
    }
  }
})
