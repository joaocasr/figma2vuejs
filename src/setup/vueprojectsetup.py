import subprocess
import os

def setup_project(name):
    r=0
    r= create_project(name)
    r= remove_boilerview(name)
    r= remove_boilercomponents(name)
    r= updateAppVue(name)
    r= tmp_routerindex(name)
    r= viteconfig(name)
    r= overwrite_styling(name)
    r= install_dependencies(name)
    return r

def create_project(name):
    r = 0
    destination = '../output/'+name
    if os.path.isdir(destination):
        print("The Vue Project "+name+" already exists.")
        r = 1
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
    return r

def remove_boilerview(name):
    r=0
    directory = '../output/'+name+'/src/views/*'
    rm = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True, text=True)
    print(rm)
    return r

def remove_boilercomponents(name):
    r=0
    directory = '../output/'+name+'/src/components/*'
    subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            capture_output=True, text=True)
    return r


def updateAppVue(name):
    r=0
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
    return r

# PASSAR PARA O GERADOR DE ROTAS
def tmp_routerindex(name):
    r=0
    router = """import { createRouter, createWebHistory } from 'vue-router'
import ErrorPageView from '@/views/ErrorPageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  },
  routes: [
  {
    path: '/:catchAll(.*)',
    name: 'error',
    component: ErrorPageView,
  }
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
        f= open(filerouter,"w")
        f.write(router)
        f.close()
    fileerror = "../output/"+name+"/src/views/ErrorPageView.vue"
    f= open(fileerror,"w")
    f.write(errorpage)
    f.close()
    return r


def viteconfig(name):
    r=0
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
    else:
        r=1
    return r

# PASSAR PARA O STYLE GENERATOR
def overwrite_styling(name):
    r=0
    maincss="""@import './base.css';
.background-container {
  max-width: 100%; 
  width: 100%; 
  margin: 0 auto;
}

@media (min-width: 1024px) {
  #app {
      padding: 0;
  }
}
#app {
  max-width: 3000px;
  max-height: auto;
  font-weight: normal;
  background-color: white;
}"""
    filemain = "../output/"+name+"/src/assets/main.css"
    f= open(filemain,"w")
    f.write(maincss)
    f.close()
    basecss= """/* color palette from <https://github.com/vuejs/theme> */
:root {
  --vt-c-white: #ffffff;
  --vt-c-white-soft: #f8f8f8;
  --vt-c-white-mute: #f2f2f2;

  --vt-c-black: #181818;
  --vt-c-black-soft: #222222;
  --vt-c-black-mute: #282828;

  --vt-c-indigo: #2c3e50;

  --vt-c-divider-light-1: rgba(60, 60, 60, 0.29);
  --vt-c-divider-light-2: rgba(60, 60, 60, 0.12);
  --vt-c-divider-dark-1: rgba(84, 84, 84, 0.65);
  --vt-c-divider-dark-2: rgba(84, 84, 84, 0.48);

  --vt-c-text-light-1: var(--vt-c-indigo);
  --vt-c-text-light-2: rgba(60, 60, 60, 0.66);
  --vt-c-text-dark-1: var(--vt-c-white);
  --vt-c-text-dark-2: rgba(235, 235, 235, 0.64);
}

/* semantic color variables for this project */
:root {
  --color-background: var(--vt-c-white);
  --color-background-soft: var(--vt-c-white-soft);
  --color-background-mute: var(--vt-c-white-mute);

  --color-border: var(--vt-c-divider-light-2);
  --color-border-hover: var(--vt-c-divider-light-1);

  --color-heading: var(--vt-c-text-light-1);
  --color-text: var(--vt-c-text-light-1);

  --section-gap: 160px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--vt-c-black);
    --color-background-soft: var(--vt-c-black-soft);
    --color-background-mute: var(--vt-c-black-mute);

    --color-border: var(--vt-c-divider-dark-2);
    --color-border-hover: var(--vt-c-divider-dark-1);

    --color-heading: var(--vt-c-text-dark-1);
    --color-text: var(--vt-c-text-dark-2);
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  font-weight: normal;
}

body {
  min-height: 100vh;
  transition:
    color 0.5s,
    background-color 0.5s;
  line-height: 1.6;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
  font-size: 15px;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color-scheme: only light;
  background-color: white;
}"""
    filebase = "../output/"+name+"/src/assets/base.css"
    f= open(filebase,"w")
    f.write(basecss)
    f.close()
    return r


def install_dependencies(name):
    r=0
    print("Downloading dependencies...")
    subprocess.run(['npm',
                    'install'],
                    cwd='../output/'+name,capture_output=True, text=True)
    return r
