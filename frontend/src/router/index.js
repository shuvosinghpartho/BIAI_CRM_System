import { ref } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import PipelineView from '../views/PipelineView.vue'
import AddEnquiryView from '../views/AddEnquiryView.vue'
import OtherEnquiriesView from '../views/OtherEnquiriesView.vue'
import SummaryView from '../views/SummaryView.vue'
import { setDynamicFavicon } from '../utils/dynamicFavicon'

export const isNavigating = ref(false)

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

router.beforeEach((to, from, next) => {
  if (to.path !== from.path) {
    isNavigating.value = true
  }
  next()
})

router.afterEach((to) => {
  setDynamicFavicon(to.path, 0)
  setTimeout(() => {
    isNavigating.value = false
  }, 380)
})

export default router
