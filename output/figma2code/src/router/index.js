import { createRouter, createWebHistory } from 'vue-router';import GenericPageView from '@/views/GenericPageView.vue';
import ErrorPageView from '@/views/ErrorPageView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    "path": "/genericpage",
    "name": "GenericPage",
    "component": GenericPageView
},
{
    "path": "/:catchAll(.*)",
    "name": "error",
    "component": ErrorPageView
},
  ]
})
export default router
