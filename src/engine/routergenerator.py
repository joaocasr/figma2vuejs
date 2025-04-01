import os
import json
import re

def generate_routes(name,pages):
    print("Updating routes...")
    element_routes = []
    for pagina in pages:
        element = {
                "component": {
                    'path': getFormatedName(pages[pagina].getPagepath()).lower(),
                    'name': getFormatedName(pages[pagina].getPagename()),
                    'component': getFormatedName(pages[pagina].getPagename())+'View',
                },
                "import": "import "+getFormatedName(pages[pagina].getPagename())+'View'+" from '@/views/"+getFormatedName(pages[pagina].getPagename())+'View'+".vue';\n"

        }
        element_routes.append(element)
    element_routes.append({
        "component":{
            'path': '/:catchAll(.*)',
            'name': 'error',
            'component': 'ErrorPageView'
        },
       "import": "import ErrorPageView from '@/views/ErrorPageView.vue';\n"
    })
    allRoutes = ""
    allImports = ""
    for e in element_routes:  
        allRoutes += json.dumps(e["component"], indent=4)+",\n"
        allImports += e["import"]
    allRoutes = re.sub(r'component": "(.*)"',r'component": \1' , allRoutes)
    router = """import { createRouter, createWebHistory } from 'vue-router';
"""+allImports+"""
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  """+allRoutes[:-1]+"""
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
        f = open(filerouter,"w")
        f.write(router)
        f.close()
    else:
        raise Exception("index.js from router folder not found!")
    fileerror = "../output/"+name+"/src/views/ErrorPageView.vue"
    f= open(fileerror,"w")
    f.write(errorpage)
    f.close()

def getFormatedName(name):
    pattern = "[\s\.\-;#:]"
    name = re.sub(pattern,"",name)
    return name