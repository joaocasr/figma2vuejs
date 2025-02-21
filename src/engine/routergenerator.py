import os

def tmp_routerindex(name):
    print("Updating routes...")
    router = """import { createRouter, createWebHistory } from 'vue-router'
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
"""
    errorpage= """<template>
        <h4>ERROR PAGE</h4>
    </template>

<script>
export default {
    data(){
        return {
        }
    },
    methods:{
    }
}
</script>

"""
    filerouter = "../output/"+name+"/src/router/index.js"
    if os.path.isfile(filerouter):
        f= open(filerouter,"w")
        f.write(router)
        f.close()
    else:
        raise Exception("index.js from router folder not found!")
    fileerror = "../output/"+name+"/src/views/ErrorPageView.vue"
    f= open(fileerror,"w")
    f.write(errorpage)
    f.close()