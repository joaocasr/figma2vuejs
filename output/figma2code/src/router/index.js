import { createRouter, createWebHistory } from 'vue-router';
import BlogPageView from '@/views/BlogPageView.vue';
import ErrorPageView from '@/views/ErrorPageView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    "path": "/blogpage",
    "name": "BlogPage",
    "component": BlogPageView
},
{
    "path": "/:catchAll(.*)",
    "name": "error",
    "component": ErrorPageView
},
  ]
})
export default router
