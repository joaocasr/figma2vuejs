from setup.vueprojectsetup import create_project


router = """import { createRouter, createWebHistory } from 'vue-router'
__IMPORT_PAGE_PLACEHOLDER__

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    __ROUTE_PLACEHOLDER__
  ],
})

export default router
"""

view = """<template>
    __TEMPLATE_PLACEHOLDER__
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
<style scoped>


</style>
"""

create_project("test1")