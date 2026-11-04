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
    theme: localStorage.getItem('biai_theme') || 'light',
    toasts: [],
    activeModalEnquiry: null,
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
    initTheme() {
      const saved = localStorage.getItem('biai_theme') || 'light'
      this.theme = saved
      document.documentElement.setAttribute('data-theme', saved)
    },

    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light'
      localStorage.setItem('biai_theme', this.theme)
      document.documentElement.setAttribute('data-theme', this.theme)
      this.showToast(`Switched to ${this.theme} theme`, 'info')
    },

    showToast(message, type = 'success') {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, message, type })
      setTimeout(() => {
        this.toasts = this.toasts.filter(t => t.id !== id)
      }, 3500)
    },

    removeToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    },

    openDetailModal(enquiry) {
      this.activeModalEnquiry = { ...enquiry }
    },

    closeDetailModal() {
      this.activeModalEnquiry = null
    },

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
        this.error = err.message
        this.showToast(err.message, 'error')
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
        if (this.activeModalEnquiry && this.activeModalEnquiry.id === id) {
          this.activeModalEnquiry = res.data
        }
        // Update overdue list
        this.overdueList = this.overdueList.filter(o => o.id !== id)
        this.showToast(`Status updated to "${newStatus}"`, 'success')
        return res.data
      } catch (err) {
        this.error = err.message
        this.showToast(`Failed to update status: ${err.message}`, 'error')
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
        this.showToast('Enquiry saved to CRM successfully!', 'success')
        return res.data
      } catch (err) {
        this.error = err.message
        this.showToast(`Save error: ${err.message}`, 'error')
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
        if (this.activeModalEnquiry && this.activeModalEnquiry.id === id) {
          this.activeModalEnquiry = null
        }
        this.showToast('Enquiry deleted', 'info')
      } catch (err) {
        this.error = err.message
        this.showToast(`Delete error: ${err.message}`, 'error')
        throw err
      }
    }
  }
})
