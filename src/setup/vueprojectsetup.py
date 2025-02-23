import subprocess
import os

def setup_project(name):
    create_project(name)
    remove_boilerview(name)
    remove_boilercomponents(name)
    updateAppVue(name)
    viteconfig(name)
    install_dependencies(name)


def create_project(name):
    destination = '../output/'+name
    if os.path.isdir(destination):
        cssdirectory = destination+"/src/assets/"

        subprocess.run(["find "+ cssdirectory +" -type f -not \( -name 'main.css' -or -name 'base.css' -or -name 'logo.svg' \) -delete"],shell=True)
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


def remove_boilercomponents(name):
    print("Removing boilerplate code from components folder...")
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
    if rm.returncode != 0:
      raise Exception("Error while installing dependencies!")  
