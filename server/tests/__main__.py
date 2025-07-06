import shutil
import requests
import time

def test_all():
    for i in range(0,36):
        print(f"Converting prototype "+str(i+1)+" to Vue.js project...")
        response = requests.get("http://localhost:8000/test/"+str(i+1))
        projectname = response.text.replace('"','')
        shutil.copytree("/home/joao/figma2vuejs/server/output/"+projectname+"/src", "/home/joao/vue-generated/usecase"+str(i+1)+"/src", dirs_exist_ok=True)
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/"+projectname+".sh", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/index.html", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/jsconfig.json", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/package.json", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/package-lock.json", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/README.md", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        shutil.copy("/home/joao/figma2vuejs/server/output/"+projectname+"/vite.config.js", "/home/joao/vue-generated/usecase"+str(i+1)+"/")
        time.sleep(5)

if __name__ == "__main__":
    test_all()
    
