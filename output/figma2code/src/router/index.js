import { createRouter, createWebHistory } from 'vue-router';
import HomePageView from '@/views/HomePageView.vue';
import MoviePageView from '@/views/MoviePageView.vue';
import WatchlistPageView from '@/views/WatchlistPageView.vue';
import ReviewPageView from '@/views/ReviewPageView.vue';
import LoginPageView from '@/views/LoginPageView.vue';
import ErrorPageView from '@/views/ErrorPageView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    "path": "/homepage",
    "name": "HomePage",
    "component": HomePageView
},
{
    "path": "/moviepage",
    "name": "MoviePage",
    "component": MoviePageView
},
{
    "path": "/watchlistpage",
    "name": "WatchlistPage",
    "component": WatchlistPageView
},
{
    "path": "/reviewpage",
    "name": "ReviewPage",
    "component": ReviewPageView
},
{
    "path": "/loginpage",
    "name": "LoginPage",
    "component": LoginPageView
},
{
    "path": "/:catchAll(.*)",
    "name": "ErrorPage",
    "component": ErrorPageView
},
  ]
})
export default router
