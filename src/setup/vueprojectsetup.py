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
        print("Removing the view files from previous generation...")
        remove_boilerview(name)
        print("Removing the component files from previous generation...")
        remove_boilercomponents(name,1)
        print("Updating main.js file...")
        updateMainJSfile(name)
        print("Injecting plugin files...")
        createPluginFiles(name)

        raise Exception("The Vue Project "+name+" already exists.")
    else:
        print("Creating Vue project named: "+name+" ...")
        subprocess.run(['npm',
                        'create',
                        'vue@latest',
                        name,
                        '--',
                        '--router',
                        '--pinia',
                        '--name',
                        name],cwd='../output/',capture_output=True, text=True)

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


def updateAppVue(name):
    print("Removing boilerplate code from App.vue...")
    appvue = """<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <RouterView></RouterView>
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

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import usePrimeVue from './plugins/primevue';

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(router)

usePrimeVue(app)


app.mount('#app')
"""
  filemain = "../output/"+name+"/src/main.js"
  f= open(filemain,"w")
  f.write(content)
  f.close()

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
  else:
    print("VSelect is already imported.")

  

def useIconFieldPrimevuePlugin(name):
  global allDependencies
  content =""
  if("inputtext" not in allDependencies or "inputicon" not in allDependencies or "iconfield" not in allDependencies==False):
    filemain = "../output/"+name+"/src/plugins/primevue.js"
    primeimport = """import InputText from 'primevue/inputtext';
import InputIcon from 'primevue/inputicon';
import IconField from 'primevue/iconfield';
"""
    primecomponent = """app.component('InputText',InputText)
app.component('InputIcon',InputIcon)
app.component('IconField',IconField)
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
    allDependencies["inputtext"]=True
    allDependencies["inputicon"]=True
    allDependencies["iconfield"]=True
  else:
    print("SearchFilter is already imported.")

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
  else:
    print("DatePicker is already imported.")


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
  else:
    print("Slider is already imported.")
