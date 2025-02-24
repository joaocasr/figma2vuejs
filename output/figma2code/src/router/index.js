import { createRouter, createWebHistory } from 'vue-router';import PrincipalPageView from '@/views/PrincipalPageView.vue';
import SecondaryPageView from '@/views/SecondaryPageView.vue';
import ErrorPageView from '@/views/ErrorPageView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    "path": "/principalpage",
    "name": "PrincipalPage",
    "component": PrincipalPageView
},
{
    "path": "/secondarypage",
    "name": "SecondaryPage",
    "component": SecondaryPageView
},
{
    "path": "/:catchAll(.*)",
    "name": "error",
    "component": ErrorPageView
},
  ]
})
export default router
