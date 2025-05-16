import subprocess
import os

allDependencies = {}

def setup_project(name):
    create_project(name)
    remove_boilerview(name)
    remove_boilercomponents(name,0)
    updateAppVue(name)
    viteconfig(name)
    install_dependencies(name)
    updateMainJSfile(name)
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
        print("Updating main.js file...")
        updateMainJSfile(name)
        print("Create toast store...")
        createToastStorefile(name)
        print("Injecting plugin files...")
        createPluginFiles(name)

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
        print(out)
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


def install_dependencies(name):
    print("Downloading dependencies...")
    rm =  subprocess.run(['npm',
                    'install'],
                    cwd='../output/'+name,capture_output=True, text=True)
    installPrimeVueDependencies(name)
    installVuetifyDependencies(name)
    if rm.returncode != 0:
      raise Exception("Error while installing dependencies!")  

def updateMainJSfile(name):
  content ="""import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ToastService from 'primevue/toastservice';

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import usePrimeVue from './plugins/primevue';

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(ToastService)
app.use(router)

usePrimeVue(app)


app.mount('#app')
"""
  filemain = "../output/"+name+"/src/main.js"
  f= open(filemain,"w")
  f.write(content)
  f.close()

def createToastStorefile(name):
  toaststorecontent="""import { defineStore } from 'pinia'
import { useToast } from "primevue/usetoast";

export const useToastStore = defineStore('toast', () => {
  const toast = useToast();


  function showSuccess (message)  {
    toast.add({ severity: 'success', summary: "Success", detail: message, life: 3000 });
  }

  function showInfo (message)  {
    toast.add({ severity: 'info', summary: "Info", detail: message, life: 3000 });
  }

  function showError (message)  {
    toast.add({ severity: 'error', summary: "Error", detail: message, life: 3000 });
  }

  return { showSuccess , showInfo, showError }
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
  fileprimevue = "../output/"+name+"/src/plugins/primevue.js"
  if not os.path.exists(plugins):
    os.makedirs(plugins)
  with open(fileprimevue,"w") as f:
    f.write(primevue)
  filevuetify = "../output/"+name+"/src/plugins/vuetify.js"
  with open(filevuetify,"w") as f:
    f.write(vuetify)

def installVuetifyDependencies(name):
  vuetify =  subprocess.run(['npm','ls','vuetify'],cwd='../output/'+name,capture_output=True, text=True)
  if("vuetify" not in vuetify.stdout):
    print("Installing Vuetify Dependencies...")
    vuetify =  subprocess.run(['npm','install','vuetify'],cwd='../output/'+name,capture_output=True, text=True)
    mdifont =  subprocess.run(['npm','install','@mdi/font'],cwd='../output/'+name,capture_output=True, text=True)
  else:
    print("Vuetify is already installed.")


def installPrimeVueDependencies(name):
  primevue =  subprocess.run(['npm','ls','primevue'],cwd='../output/'+name,capture_output=True, text=True)
  if("primevue" not in primevue.stdout):
    print("Installing PrimeVue Dependencies...")
    primevue =  subprocess.run(['npm','install','primevue'],cwd='../output/'+name,capture_output=True, text=True)
    primeicons =  subprocess.run(['npm','install','primeicons'],cwd='../output/'+name,capture_output=True, text=True)
    primevuethemes =  subprocess.run(['npm','install','@primevue/themes'],cwd='../output/'+name,capture_output=True, text=True)
    primeforms =  subprocess.run(['npm','install','@primevue/forms'],cwd='../output/'+name,capture_output=True, text=True)
    allDependencies["primevue"]=True
  else:
    print("PrimeVue is already installed.")

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
    selectimport = "import { VRating } from 'vuetify/components';\n"
    componentname ="\tVRating"
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
