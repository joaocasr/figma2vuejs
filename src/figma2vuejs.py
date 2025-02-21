from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from parser.modelconverter import getFigmaData

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
project_name, pages = getFigmaData()

try:
  setup_project(project_name)
  overwrite_styling(project_name)
except Exception as e:
  print(e)

generate_routes(project_name,pages)
