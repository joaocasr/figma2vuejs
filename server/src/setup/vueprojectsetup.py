from engine.stylegenerator import overwrite_styling
import subprocess
import os

vuetifydependencies = {}
primevuedependencies = {}

def VueSetup():
  global vuetifydependencies,primevuedependencies
  vuetifydependencies = {}
  primevuedependencies = {}

def setup_project(name):
  create_project(name)
  overwrite_styling(name)
  remove_boilerview(name)
  remove_boilercomponents(name,0)
  updateAppVue(name)
  viteconfig(name)
    
def create_project(name):
    destination = '../output/'+name
    if os.path.isdir(destination):
        cssdirectory = destination+"/src/assets/"

        print("The Vue Project "+name+" already exists.")
        print("Removing the css files from previous generation...")
        subprocess.run(["find "+ cssdirectory +" -type f -not \( -name 'main.css' -or -name 'base.css' -or -name 'logo.svg' \) -delete"],shell=True)
        print("Removing view files from previous generation...")
        remove_boilerview(name)
        print("Removing component files from previous generation...")
        remove_boilercomponents(name,1)
        print("Removing store files from previous generation...")
        remove_boilerstore(name,1)
        print("Removing plugin files from previous generation...")
        remove_pluginfiles(name,1)
        print("Updating App.vue")
        updateAppVue(name)
        print("Updating vite.config")
        viteconfig(name)
        print("Overwrite global styling.")
        overwrite_styling(name)
        print("Create toast store...")
        createToastStorefile(name)

        raise Exception("The Vue Project "+name+" already exists.")
    else:
        print("Creating Vue project named: "+name+" ...")
        out = subprocess.run(['npm',
                        'create',
                        'vue@latest',
                        name,
                        '--',
                        '--router',
                        '--pinia',
                        ],cwd='../output/',capture_output=True,text=True)
        if out.returncode != 0:
          raise Exception("Error creating Vue project "+name)

def remove_boilerview(name):
    directory = '../output/'+name+'/src/views/*'
    rm = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True)
    if rm.returncode != 0:
      raise Exception("Error while cleaning boilerplate code from the view folder!")


def remove_boilercomponents(name,n):
    if(n==0): print("Removing boilerplate code from components folder...")
    directory = '../output/'+name+'/src/components/*'
    rm = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while cleaning boilerplate code from the components folder!")    

def remove_boilerstore(name,n):
    if(n==0): print("Removing boilerplate code from stores folder...")
    directory = '../output/'+name+'/src/stores/*'
    rm = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while cleaning boilerplate code from the stores folder!")    

def remove_pluginfiles(name,n):
    if(n==0): print("Removing plugin files...")
    directory = '../output/'+name+'/src/plugins/*'
    rm = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while removing plugin files!")    

def updatingPluginFiles(name):
  global primevuedependencies,vuetifydependencies
  primevueplugin = '../output/'+name+'/src/plugins/primevue.js'
  vuetifyplugin = '../output/'+name+'/src/plugins/vuetify.js'
  if(len(primevuedependencies)==0):
    rm = subprocess.run(['sh',
                              '-c',
                              'rm '+ primevueplugin],
                              capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while removing primevue plugin files!")    

  if(len(vuetifydependencies)==0):
    rm = subprocess.run(['sh',
                              '-c',
                              'rm '+ vuetifyplugin],
                              capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while removing vuetify plugin files!")    

def updateAppVue(name):
    print("Removing boilerplate code from App.vue...")
    appvue = """<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView></RouterView>
  <Toast></Toast>
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
    file = "../output/"+name+"/src/App.vue"
    if os.path.isfile(file):
        f= open(file,"w")
        f.write(appvue)
        f.close()
    else: raise Exception("App.vue file not found!")


def viteconfig(name):
    print("Removing dev tools functionalities in vite file...")
    viteconfig= """import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})"""
    filevite = "../output/"+name+"/vite.config.js"
    if os.path.isfile(filevite):
        f= open(filevite,"w")
        f.write(viteconfig)
        f.close()
    else: raise Exception("vite.config.js file not found!")

def updateMainJSfile(name):
  global primevuedependencies,vuetifydependencies
  importvuetify = "import vuetify from './plugins/vuetify';"
  importprimevue = "import usePrimeVue from './plugins/primevue';"
  usevuetify = "app.use(vuetify)"
  useprimevue = "usePrimeVue(app)"
  if(len(primevuedependencies)==0): 
    importprimevue = ""
    useprimevue = ""
  if(len(vuetifydependencies)==0):
    importvuetify = ""
    usevuetify = ""
  content =f"""import './assets/main.css'

import"""+ "{ createApp }"+ """from 'vue'
import"""+ "{ createPinia }"+ f"""from 'pinia'
import ToastService from 'primevue/toastservice';
{importvuetify}
{importprimevue}

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
{usevuetify}
app.use(ToastService)
app.use(router)

{useprimevue}

app.mount('#app')
"""
  filemain = "../output/"+name+"/src/main.js"
  f= open(filemain,"w")
  f.write(content)
  f.close()

def createToastStorefile(name):
  toaststorecontent="""import { defineStore } from 'pinia'
import { useToast } from "primevue/usetoast";

export const useToastStore = defineStore('toast', {
  state: () => ({
    toast: useToast(),
    allToasts : []
  }),
  getters: {
    getToasts(state) { return state.allToasts}
  },
  actions: {
    showSuccess(message) {
       this.toast.add({ severity: 'success', summary: "Success", detail: message, life: 3000 })
       this.allToasts.push({ severity: 'success', summary: "Success", detail: message, timestamp: Date() })
      },
    showInfo(message) {
       this.toast.add({ severity: 'info', summary: "Info", detail: message, life: 3000 })
       this.allToasts.push({ severity: 'info', summary: "Info", detail: message, timestamp: Date() })
      },
    showError(message){
      this.toast.add({ severity: 'error', summary: "Error", detail: message, life: 3000 })
      this.allToasts.push({ severity: 'error', summary: "Error", detail: message, timestamp: Date() })
    }
  }
})
"""
  stores = "../output/"+name+"/src/stores/"
  toaststore = "../output/"+name+"/src/stores/toast.js"
  if not os.path.exists(stores):
    os.makedirs(stores)
  with open(toaststore,"w") as f:
    f.write(toaststorecontent)

def injectPluginComponents(name):
  global primevuedependencies,vuetifydependencies
  primevueimports = ""
  useprimevuecompoents = ""
  vuetifyimports = "import { "
  usevuetifycompoents = ""
  for d in primevuedependencies:
    if(d=="Form"): primevueimports+="import { Form } from '@primevue/forms';\n"
    else: primevueimports+="import "+ d +" from 'primevue/"+d.lower()+"';\n"
    useprimevuecompoents+=f"app.component('{d}',{d})"+"\n"
  for d in vuetifydependencies:
    vuetifyimports+=d+","
    usevuetifycompoents+="  "+d+",\n"
  if(len(vuetifyimports)==9): vuetifyimports=""
  if(len(vuetifyimports)>=2): vuetifyimports=vuetifyimports[:-1]
  if(len(vuetifyimports)>9): vuetifyimports+="} from 'vuetify/components';"
  if(len(usevuetifycompoents)>=3): usevuetifycompoents=usevuetifycompoents[:-2]
  primevue=f"""import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';
{primevueimports}
"""+"""
export default function usePrimeVue(app){
    
    app.use(PrimeVue, {
      theme: {
        preset: Material
    }
    });
  """+f"""
{useprimevuecompoents}"""+"""
}
"""
  vuetify="""import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css';"""+f"""
{vuetifyimports}
"""+"""
const vuetify = createVuetify({
    components: {"""+usevuetifycompoents+"""},
    icons: {
        defaultSet: 'mdi',
    }
})

export default vuetify;
"""
  plugins = "../output/"+name+"/src/plugins/"
  if not os.path.exists(plugins):
    os.makedirs(plugins)
  fileprimevue = "../output/"+name+"/src/plugins/primevue.js"
  with open(fileprimevue,"w") as f:
    f.write(primevue)
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  with open(filevuetify,"w") as f:
    f.write(vuetify)

def useSelectVuetifyPlugin(name):
  global vuetifydependencies
  if("VSelect" not in vuetifydependencies):
    vuetifydependencies["VSelect"]=True

def useRatingVuetifyPlugin(name):
  global vuetifydependencies
  if("VRating" not in vuetifydependencies):
    vuetifydependencies["VRating"]=True

def usePaginatorVuetifyPlugin(name):
  global vuetifydependencies
  if("VPagination" not in vuetifydependencies):
    vuetifydependencies["VPagination"]=True

def useMenuVuetifyPlugin(name):
  global vuetifydependencies
  if("VMenu" not in vuetifydependencies): 
    vuetifydependencies["VMenu"]=True
  if("VList" not in vuetifydependencies):
    vuetifydependencies["VList"]=True
  if("VListItem" not in vuetifydependencies):
    vuetifydependencies["VListItem"]=True

def useFormPrimeVuePlugin(name):
  global primevuedependencies
  if("Form" not in primevuedependencies): 
    primevuedependencies["Form"]=True
  if("InputText" not in primevuedependencies):
    primevuedependencies["InputText"]=True
  if("Message" not in primevuedependencies):
    primevuedependencies["Message"]=True

def useCheckboxPrimeVuePlugin(name):
  global primevuedependencies
  if("Checkbox" not in primevuedependencies):
    primevuedependencies["Checkbox"]=True

def useIconFieldPrimevuePlugin(name):
  global primevuedependencies
  if("InputText" not in primevuedependencies): 
    primevuedependencies["InputText"]=True
  if("InputIcon" not in primevuedependencies):
    primevuedependencies["InputIcon"]=True
  if("IconField" not in primevuedependencies):
    primevuedependencies["IconField"]=True

def useDatePickerPrimevuePlugin(name):
  global primevuedependencies
  if("DatePicker" not in primevuedependencies):
    primevuedependencies["DatePicker"]=True


def useSliderPrimevuePlugin(name):
  global primevuedependencies
  if("Slider" not in primevuedependencies):
    primevuedependencies["Slider"]=True

def useDataTablePrimevuePlugin(name):
  global primevuedependencies
  if("DataTable" not in primevuedependencies): 
    primevuedependencies["DataTable"]=True
  if("Column" not in primevuedependencies):
    primevuedependencies["Column"]=True

def useToastPrimeVuePlugin(name):
  global primevuedependencies
  if("Toast" not in primevuedependencies):
    primevuedependencies["Toast"]=True

def rewriteIndexHTML(name):
  content = f"""<!DOCTYPE html>
<html lang="en" xml:lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""
  fileindex = "../output/"+name+"/index.html"
  with open(fileindex,"w") as f:
    f.write(content)

def buildDependenciesScript(name):
  global primevuedependencies,vuetifydependencies
  setup = "npm install"
  if(len(vuetifydependencies)>0):
    setup = "npm install vuetify\nnpm install @mdi/font\n" + setup
  if("form" in primevuedependencies):
    setup = "npm install @primevue/forms\n" + setup
  if(len(primevuedependencies)>0):
    setup = "npm install primevue\nnpm install primeicons\nnpm install @primevue/themes\nnpm install @primevue/themes\n" + setup
  scriptsetup = "../output/"+name+"/"+name+".sh"
  setup = "# Install project dependencies packages\n" + setup
  setup+="\n\n#Run Vue project\nnpm run build\nnpm run preview"
  with open(scriptsetup,"w") as f:
    f.write(setup)