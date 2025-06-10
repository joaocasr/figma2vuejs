import subprocess
import os

allDependencies = {}
primevuecomponents = False
vuetifycomponents = False

def setup_project(name):
  global allDependencies
  allDependencies = {}
  create_project(name)
  remove_boilerview(name)
  remove_boilercomponents(name,0)
  updateAppVue(name)
  viteconfig(name)
  createPluginFiles(name)
    
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
        print("updating plugin files")
        createPluginFiles(name)
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
  global primevuecomponents,vuetifycomponents
  primevueplugin = '../output/'+name+'/src/plugins/primevue.js'
  vuetifyplugin = '../output/'+name+'/src/plugins/vuetify.js'
  if(primevuecomponents==False):
    rm = subprocess.run(['sh',
                              '-c',
                              'rm '+ primevueplugin],
                              capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while removing primevue plugin files!")    

  if(vuetifycomponents==False):
    rm = subprocess.run(['sh',
                              '-c',
                              'rm '+ vuetifyplugin],
                              capture_output=True, text=True)
    if rm.returncode != 0:
      raise Exception("Error while removing vuetify plugin files!")    

def updateAppVue(name):
    print("Removing boilerplate code from App.vue...")
    appvue = """<script setup>
import { RouterLink, RouterView } from 'vue-router'
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
  global primevuecomponents, vuetifycomponents
  importvuetify = "import vuetify from './plugins/vuetify';"
  importprimevue = "import usePrimeVue from './plugins/primevue';"
  usevuetify = "app.use(vuetify)"
  useprimevue = "usePrimeVue(app)"
  if(primevuecomponents==False): 
    importprimevue = ""
    useprimevue = ""
  if(vuetifycomponents==False):
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

def createPluginFiles(name):
  print("creating plugin files...")
  primevue="""import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';


export default function usePrimeVue(app){
    
    app.use(PrimeVue, {
      theme: {
        preset: Material
    }
    });
  
}
"""
  vuetify="""import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css';

const vuetify = createVuetify({
    components: {},
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
  global allDependencies
  content =""
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  if("vselect" not in allDependencies):
    selectimport = "import { VSelect } from 'vuetify/components';\n"
    componentname ="\tVSelect"
    f = open(filevuetify, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import '@mdi/font/css/materialdesignicons.css';"):
        content+=selectimport
      if(l=="components: {},"):
        content=content[:-3] +"\n"+ componentname + "\n},\n"
      if(l=="components: {"):
        content+= componentname + ",\n"
    f.close()
    f= open(filevuetify,"w")
    f.write(content)
    f.close()
    allDependencies["vselect"]=True

def useRatingVuetifyPlugin(name):
  global allDependencies
  content =""
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  if("vrating" not in allDependencies):
    ratingimport = "import { VRating } from 'vuetify/components';\n"
    componentname ="\tVRating"
    f = open(filevuetify, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import '@mdi/font/css/materialdesignicons.css';"):
        content+=ratingimport
      if(l=="components: {},"):
        content=content[:-3] +"\n"+ componentname + "\n},\n"
      if(l=="components: {"):
        content+= componentname + ",\n"
    f.close()
    f= open(filevuetify,"w")
    f.write(content)
    f.close()
    allDependencies["vrating"]=True

def usePaginatorVuetifyPlugin(name):
  global allDependencies
  content =""
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  if("vpagination" not in allDependencies):
    selectimport = "import { VPagination } from 'vuetify/components';\n"
    componentname ="\tVPagination"
    f = open(filevuetify, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import '@mdi/font/css/materialdesignicons.css';"):
        content+=selectimport
      if(l=="components: {},"):
        content=content[:-3] +"\n"+ componentname + "\n},\n"
      if(l=="components: {"):
        content+= componentname + ",\n"
    f.close()
    f= open(filevuetify,"w")
    f.write(content)
    f.close()
    allDependencies["vpagination"]=True

def useMenuVuetifyPlugin(name):
  global allDependencies
  content =""
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  if("vmenu" not in allDependencies or "vlist" not in allDependencies or "vlistitem" not in allDependencies):
    vuetifyimport = ""
    vuetifycomponent = ""
    components = []
    if("vmenu" not in allDependencies): 
      vuetifyimport+="""import { VMenu } from 'vuetify/components';\n"""
      components.append("VMenu")
    if("vlist" not in allDependencies):
      vuetifyimport+="""import { VList } from 'vuetify/components';\n"""
      components.append("VList")
    if("vlistitem" not in allDependencies):
      vuetifyimport+="""import { VListItem } from 'vuetify/components';\n"""
      components.append("VListItem")

    vuetifycomponents = ',\n\t'.join(components)
    f = open(filevuetify, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import '@mdi/font/css/materialdesignicons.css';"):
        content+=vuetifyimport
      if(l=="components: {},"):
        content=content[:-3] +"\n"+ vuetifycomponents + "\n},\n"
      if(l=="components: {"):
        content+= vuetifycomponents + ",\n"
    f.close()
    f= open(filevuetify,"w")
    f.write(content)
    f.close()
    allDependencies["vmenu"]=True
    allDependencies["vlist"]=True
    allDependencies["vlistitem"]=True

def useFormPrimeVuePlugin(name):
  global allDependencies
  content =""
  if("form" not in allDependencies or "inputtext" not in allDependencies or "message" not in allDependencies==False):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = ""
    primecomponent = ""
    if("form" not in allDependencies): 
      primeimport+="""import { Form } from '@primevue/forms';\n"""
      primecomponent+="""app.component('Form',Form)\n"""
    if("inputtext" not in allDependencies):
      primeimport+="""import InputText from 'primevue/inputtext';\n"""
      primecomponent+="""app.component('InputText',InputText)\n"""
    if("message" not in allDependencies):
      primeimport+="""import Message from 'primevue/message';\n"""
      primecomponent+="""app.component('Message',Message)\n"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["form"]=True
    allDependencies["inputtext"]=True
    allDependencies["message"]=True

def useCheckboxPrimeVuePlugin(name):
  global allDependencies
  content =""
  if("checkbox" not in allDependencies):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = ""
    primecomponent = ""
    if("checkbox" not in allDependencies): 
      primeimport+="""import Checkbox from 'primevue/checkbox';\n"""
      primecomponent+="""app.component('Checkbox',Checkbox)\n"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["checkbox"]=True

def useIconFieldPrimevuePlugin(name):
  global allDependencies
  content =""
  if("inputtext" not in allDependencies or "inputicon" not in allDependencies or "iconfield" not in allDependencies==False):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = ""
    primecomponent = ""
    if("inputtext" not in allDependencies): 
      primeimport+="""import InputText from 'primevue/inputtext';\n"""
      primecomponent+="""app.component('InputText',InputText)\n"""
    if("inputicon" not in allDependencies):
      primeimport+="""import InputIcon from 'primevue/inputicon';\n"""
      primecomponent+="""app.component('InputIcon',InputIcon)\n"""
    if("iconfield" not in allDependencies):
      primeimport+="""import IconField from 'primevue/iconfield';\n"""      
      primecomponent+="""app.component('IconField',IconField)\n"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["inputtext"]=True
    allDependencies["inputicon"]=True
    allDependencies["iconfield"]=True

def useDatePickerPrimevuePlugin(name):
  global allDependencies
  content =""
  if("datepicker" not in allDependencies):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = """import DatePicker from 'primevue/datepicker';
"""
    primecomponent = """app.component('DatePicker',DatePicker)
"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["datepicker"]=True


def useSliderPrimevuePlugin(name):
  global allDependencies
  content =""
  if("slider" not in allDependencies):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = """import Slider from 'primevue/slider';
"""
    primecomponent = """app.component('Slider',Slider)
"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["slider"]=True

def useDataTablePrimevuePlugin(name):
  global allDependencies
  content =""
  if("datatable" not in allDependencies or "column" not in allDependencies):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = ""
    primecomponent = ""
    if("datatable" not in allDependencies): 
      primeimport+="""import DataTable from 'primevue/datatable';\n"""
      primecomponent+="""app.component('DataTable',DataTable)\n"""
    if("column" not in allDependencies):
      primeimport+="""import Column from 'primevue/column';\n"""
      primecomponent+="""app.component('Column',Column)\n"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["datatable"]=True
    allDependencies["column"]=True

def useToastPrimeVuePlugin(name):
  global allDependencies
  content =""
  if("toast" not in allDependencies):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport="""import Toast from 'primevue/toast';\n"""
    primecomponent="""app.component('Toast',Toast);\n"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import 'primeicons/primeicons.css';"):
        content+=primeimport
      if(l=="});"):
        content+=primecomponent
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["toast"]=True

def buildDependenciesScript(name):
  global allDependencies, primevuecomponents, vuetifycomponents
  setup = "npm install"
  if("vselect" in allDependencies or "vrating" in allDependencies or "vpagination" in allDependencies or
     "vpagination" in allDependencies or "vmenu" in allDependencies or "vlist" in allDependencies or "vlistitem" in allDependencies):
    setup = "npm install vuetify\nnpm install @mdi/font\n" + setup
    vuetifycomponents = True
  if("form" in allDependencies):
    setup = "npm install @primevue/forms\n" + setup
    primevuecomponents = True
  if("toast" in allDependencies or "datatable" in allDependencies or "column" in allDependencies or "slider" in allDependencies or "datepicker" in allDependencies
     or "inputtext" in allDependencies or "inputicon" in allDependencies or "iconfield" in allDependencies or "checkbox" in allDependencies or
    "message" in allDependencies):
    setup = "npm install primevue\nnpm install primeicons\nnpm install @primevue/themes\nnpm install @primevue/themes\n" + setup
    primevuecomponents = True
  scriptsetup = "../output/"+name+"/"+name+".sh"
  setup = "# Install project dependencies packages\n" + setup
  setup+="\n\n#Run Vue project\nnpm run build\nnpm run preview"
  with open(scriptsetup,"w") as f:
    f.write(setup)