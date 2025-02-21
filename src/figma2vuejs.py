from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import tmp_routerindex
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
try:
  setup_project("test1")
  overwrite_styling("test1")
  tmp_routerindex("test1")
except Exception as e:
  print(e)
