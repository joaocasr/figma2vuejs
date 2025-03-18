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
        print("Updating main.js file")
        updateMainJSfile(name)
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
    if rm.returncode != 0:
      raise Exception("Error while installing dependencies!")  

def updateMainJSfile(name):
  content ="""import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
      theme: {
          preset: Material
      }
});

app.mount('#app')
"""
  filemain = "../output/"+name+"/src/main.js"
  f= open(filemain,"w")
  f.write(content)
  f.close()


def installVue3select_dependency(name):
  c =  subprocess.run(['npm','ls','vue3-select-component'],cwd='../output/'+name,capture_output=True, text=True)
  if("vue3-select-component" in c.stdout):
    print("Vue3-select-component already installed.")
  else:
    i =  subprocess.run(['npm','install','vue3-select-component'],cwd='../output/'+name,capture_output=True, text=True)
    print("Installing Vue3-select-component...")
    if(c.returncode != 0 or i.returncode != 0):
      raise Exception("Error while installing Vue3-select-component")  

def installPrimeVueDependencies(name):
  primevue =  subprocess.run(['npm','ls','primevue'],cwd='../output/'+name,capture_output=True, text=True)
  if("primevue" not in primevue.stdout):
    print("Installing PrimeVue Dependencies...")
    primevue =  subprocess.run(['npm','install','primevue'],cwd='../output/'+name,capture_output=True, text=True)
    primeicons =  subprocess.run(['npm','install','primeicons'],cwd='../output/'+name,capture_output=True, text=True)
    primevuethemes =  subprocess.run(['npm','install','@primevue/themes'],cwd='../output/'+name,capture_output=True, text=True)
    filemain = "../output/"+name+"/src/main.js"
    content = ""
    primevueimports = """import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';
"""
    primevueuse = """app.use(PrimeVue, {
      theme: {
          preset: Material
      }
});"""
    f = open(filemain, "r")
    for l in f.readlines():
      l = l.strip()
      content+=l+"\n"
      if(l=="import { createPinia } from 'pinia'"):
        content+=primevueimports+"\n"
      if(l=="app.use(router)"):
        content+=primevueuse+"\n"
    print(content)
    f.close()
    f= open(filemain,"w")
    f.write(content)
    f.close()
    allDependencies["primevue"]=True
  else:
    print("PrimeVue is already installed.")

def useIconFieldPrimevuePlugin(name):
  global allDependencies
  content =""
  if("inputtext" not in allDependencies or "inputicon" not in allDependencies or "iconfield" not in allDependencies==False):
    filemain = "../output/"+name+"/src/main.js"
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
    filemain = "../output/"+name+"/src/main.js"
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
    filemain = "../output/"+name+"/src/main.js"
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
