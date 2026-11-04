import { createRouter, createWebHistory } from 'vue-router'
import PipelineView from '../views/PipelineView.vue'
import AddEnquiryView from '../views/AddEnquiryView.vue'
import OtherEnquiriesView from '../views/OtherEnquiriesView.vue'
import SummaryView from '../views/SummaryView.vue'

const routes = [
  {
    path: '/',
    name: 'pipeline',
    component: PipelineView,
    meta: { title: 'Sales Pipeline' }
  },
  {
    path: '/add',
    name: 'add-enquiry',
    component: AddEnquiryView,
    meta: { title: 'Add New Enquiry' }
  },
  {
    path: '/other',
    name: 'other-enquiries',
    component: OtherEnquiriesView,
    meta: { title: 'Other Enquiries' }
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryView,
    meta: { title: 'Weekly Summary & Reports' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
