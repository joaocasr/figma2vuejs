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
    if(newx==None and len(pages)>0):
        element_routes.append({
                    "component":{
                        'path': '/:catchAll(.*)',
                        'name': 'ErrorPage',
                        'component': 'ErrorPageView'
                    },
                "import": "import ErrorPageView from '@/views/ErrorPageView.vue';\n"
                })
        background = "background-color:rgba(0,0,0,0);"
        if(pages[pagina].style.backgroundColor!=None):
            background = """\n  background-color:"""+ pages[pagina].style.backgroundColor+";\n"
        if(pages[pagina].style.background!=None):
            background = """\n  background:"""+ pages[pagina].style.background+";\n"
        pagepath = element_routes[0]["component"]["path"]
        pagename = element_routes[0]["component"]["name"]
        errorpage= get_Errorpage(pagename,pagepath)
        errorpagecss = get_Errorpagecss(background)
        filerror = "../output/"+name+"/src/views/ErrorPageView.vue"
        with open(filerror,"w") as f:
            f.write(errorpage)
        filerrorcss = "../output/"+name+"/src/assets/errorpage.css"
        with open(filerrorcss,"w") as f:
            f.write(errorpagecss)
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
        
def get_Errorpage(pagename,pagepath):
    return '''<template>
    <div class="grid-container">
        <div class="grid-item carderror">
            <h1 class="grid-item txt1">Page Not Found</h1>
            <h2 class="grid-item txt2">404</h2>
        <p class="grid-item txt3">The page you are looking for doesn't exist. Return to '''+ f"{pagename}" + '''</p>
        <button @click="returntopage" class="grid-item btn1">'''+f"{pagename}" + """</button>
        </div>
    </div>
  </template>
<script>
export default{
    methods:{
        returntopage(){
            this.$router.push({path:'"""+f"{pagepath}"+"""'})
        }
    }
}
</script>
<style lang="css" scoped>
@import '../assets/errorpage.css';
</style>
"""

def get_Errorpagecss(background):
    return """
.grid-container {
  display:grid;
  grid-template-columns:repeat(64,1fr);
  grid-template-rows:repeat(128, 18.6796875px);
  width: 100%;
""" +f"{background} "+ """
  min-height: 100vh;
  max-height: auto;
  margin:0;
  padding:0;
}

.grid-item {
  display:flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
.carderror{
    grid-template-columns:repeat(64,1fr);
    grid-template-rows:repeat(64,1fr);
    background-color:white;
    opacity:0.5;
    grid-column-start: 4;
	grid-column-end: 61;
	grid-row-start: 2;
	grid-row-end: 38;
    border-radius:20px;
    display:grid;
 }
.btn1{
    background-color:black;
    color:white;
    grid-column-start: 25;
	grid-column-end: 40;
	grid-row-start: 33;
	grid-row-end: 39;
    border-radius:20px;
 } 
.txt1 {
	font-style: Regular;
	font-weight: 400;
	font-size: 67px;
	font-family: 'Inter', sans-serif;
	text-align: left;
	line-height: 80px;
	color: rgba(0.0,0.0,0.0,1.0);
    grid-column-start: 25;
	grid-column-end: 63;
	grid-row-start: 4;
	grid-row-end: 12;
	display: flex;
	overflow-wrap: break-word;
	white-space: normal;
	width: 100%;
	align-items: stretch;
	justify-content: stretch;
}


.txt2 {
	font-style: Regular;
	font-weight: 400;
	font-size: 50px;    
    font-family: 'Inter', sans-serif;
	text-align: left;
	line-height: 10px;
	color: rgba(0.0,0.0,0.0,1.0);
    grid-column-start: 31;
	grid-column-end: 68;
	grid-row-start: 12;
	grid-row-end: 22;
	display: flex;
	overflow-wrap: break-word;
	white-space: normal;
	width: 100%;
	align-items: stretch;
	justify-content: stretch;
}
.txt3 {
	font-style: Regular;
	font-weight: 400;
	font-size: 25px;
	font-family: 'Inter', sans-serif;
	text-align: left;
	color: rgba(0.0,0.0,0.0,1.0);
    grid-column-start: 20;
	grid-column-end: 63;
	grid-row-start: 24;
	grid-row-end: 33;
	display: flex;
	overflow-wrap: break-word;
	white-space: normal;
	width: 100%;
	align-items: stretch;
	justify-content: stretch;
}"""