import subprocess
import os

def create_project(name):
    r = 0
    destination = '../output/'+name
    if os.path.isdir(destination):
        print("The Vue Project "+name+" already exists.")
        r = 1
    else:
        print("Creating Vue project named: "+name+" ...")
        result = subprocess.run(['npm',
                                'create',
                                'vue@latest',
                                name,
                                '--',
                                '--router',
                                '--pinia',
                                '--name',
                                name],cwd='../output/',capture_output=True, text=True, input="y")
    return r

def remove_biolerview(name):
    directory = '../../output/'+name+'/src/views/*'
    result = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            ,capture_output=True, text=True, input="y")

def remove_biolercomponents(name):
    directory = '../../output/'+name+'/src/components/*'
    result = subprocess.run(['sh',
                            '-c',
                            'rm -rf '+ directory],
                            ,capture_output=True, text=True, input="y")
    

def updateAppVue():
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
    file = '../../output/'+name+'/src/App.vue'
    with open(file,'w') as f:
        data = f.write(appvue)
