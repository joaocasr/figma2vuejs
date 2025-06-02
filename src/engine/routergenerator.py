import json
import re
from utils.tools import getFormatedName

def generate_routes(name,pages):
    print("Updating routes...")
    element_routes = []
    for pagina in pages:
        pagename = getFormatedName(pages[pagina].getPagename())
        element = {
                "component": {
                    'path': "/"+pagename.lower(),
                    'name': pagename,
                    'component': pagename+'View',
                },
                "import": "import "+pagename+'View'+" from '@/views/"+pagename+'View'+".vue';\n"

        }
        element_routes.append(element)
    newx = None
    for x in element_routes:
        if(x["component"]['name']=="ErrorPage"):
            newx = x
            newx["component"]["path"]='/:catchAll(.*)'
            element_routes.remove(x)
            element_routes.append(newx)
    if(newx==None):
        element_routes.append({
                    "component":{
                        'path': '/:catchAll(.*)',
                        'name': 'ErrorPage',
                        'component': 'ErrorPageView'
                    },
                "import": "import ErrorPageView from '@/views/ErrorPageView.vue';\n"
                })
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
        filerror = "../output/"+name+"/src/views/ErrorPageView.vue"
        with open(filerror,"w") as f:
            f.write(errorpage)
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
    filerouter = "../output/"+name+"/src/router/index.js"
    with open(filerouter,"w") as f:
        f.write(router)