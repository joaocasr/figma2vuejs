import { createRouter, createWebHistory } from 'vue-router'
import ErrorPageView from '@/views/ErrorPageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    path: '/:catchAll(.*)',
    name: 'error',
    component: ErrorPageView,
  }
  ]
})
export default router
