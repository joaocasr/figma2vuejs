from setup.vueprojectsetup import setup_project, buildDependenciesScript, updateMainJSfile, updatingPluginFiles
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from engine.variantgenerator import writeVariantComponent
from engine.gridgenerator import generateGridTemplate
from engine.pagegenerator import buildpage
from engine.componentgenerator import buildcomponent
from parser.modelconverter import getFigmaData,extractImages,extractSVGs
from parser.model.VariantComponent import VariantComponent
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import json

import sys,os,requests
from dotenv import load_dotenv, find_dotenv

FIGMA_API_KEY = ""
FILE_KEY = ""
headers = {}
project_name = ""


prototype = None
data = None

def set_variables(filekey,token):
  global FIGMA_API_KEY, FILE_KEY, headers
  FIGMA_API_KEY = token
  FILE_KEY = filekey
  headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

def load_variables():
  global FIGMA_API_KEY, FILE_KEY, headers
  l = load_dotenv(find_dotenv())
  if l==True:
    FIGMA_API_KEY = os.environ.get("FIGMA_API_KEY")
    FILE_KEY = os.environ.get("FILE_KEY")
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}
    
def convert_prototype(testfile=None):
  global data,headers,project_name,FIGMA_API_KEY,FILE_KEY
  if(testfile==None):
    response = requests.get("https://api.figma.com/v1/files/"+FILE_KEY, headers=headers)
    data = response.json()
    if('status' in data and data['status']==404): raise 'Bad request. Verify your token and prototype url!'
  else:
    data = testfile
  # extract figma data and build intern model
  #try:
  project_name, allpages, orphanComponents, refs, variants = getFigmaData(data)
  #except Exception as e:
  #  print(e)
  #  sys.exit()

  # project setup
  try:
    setup_project(project_name)
    overwrite_styling(project_name)
  except Exception as e:
    pass

  extractImages(project_name,FIGMA_API_KEY,FILE_KEY)
  extractSVGs(project_name,FIGMA_API_KEY,FILE_KEY)

  # generate routes to the vue pages
  generate_routes(project_name,allpages)

  # pages_info will be a dictionary of the path and components ids of each page
  pagesInfo = dict()
  for page in allpages:
    pagesInfo[page] = {"path":allpages[page].pagepath,
                       "name": page, "id": allpages[page].idpage,
                       "components": allpages[page].components,
                       "pageElements":allpages[page].elements}

  mypages = allpages
  if(len(sys.argv)==4): mypages = generateGridTemplate(allpages,sys.argv[2],sys.argv[3])
  if(mypages!=None):
    allcomponents=[]
    for page in pagesInfo:
      for x in pagesInfo[page]["components"]:
        if(not any(x==c for c in allcomponents)):
          allcomponents.append(x)
   
    for component in allcomponents:
      buildcomponent(component,project_name,pagesInfo,refs,variants)

    for orphan in orphanComponents:
      if(not isinstance(orphan,VariantComponent) and not orphan.getisVariant()==True):
        buildcomponent(orphan,project_name,pagesInfo,refs,variants)
          
    for v in variants:
      writeVariantComponent(v.getNameComponent(),project_name,v.variantComponents)    
          
    # build each page (elements within, styling and components)
    for page in mypages:
      buildpage(project_name,mypages[page],pagesInfo,refs,variants)

  buildDependenciesScript(project_name)
  updateMainJSfile(project_name)
  updatingPluginFiles(project_name)

load_variables()    

origins = [
    "http://localhost:4173",
    "http://localhost:5174",
    "http://localhost:5173"

]  
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInfo(BaseModel):
  apikey: Optional[str] = None
  filekey: Optional[str] = None

@app.post("/")
async def convert_figma2vue(userinfo: UserInfo = None):
  global FIGMA_API_KEY, FILE_KEY, project_name
  if(userinfo != None and userinfo.apikey!=None and userinfo.filekey!=None):
    set_variables(userinfo.filekey,userinfo.apikey)
  if(FIGMA_API_KEY=="" and FILE_KEY==""):
    return "Missing token and prototype url!"
  else:
    try:
      convert_prototype()
    except Exception as e:
      raise HTTPException(status_code=404, detail=repr(e))
    shutil.make_archive('../output/'+project_name, format='zip', root_dir='../output')
    return project_name


# only for testing
@app.get("/")
async def convert_figma2vue(userinfo: UserInfo = None):
  global FIGMA_API_KEY, FILE_KEY, project_name
  if(userinfo != None and userinfo.apikey!=None and userinfo.filekey!=None):
    set_variables(userinfo.filekey,userinfo.apikey)
  if(FIGMA_API_KEY=="" and FILE_KEY==""):
    return "Missing token and prototype url!"
  else:
    convert_prototype()
    return project_name

# only for testing
@app.get("/test/{nr}")
def convert_figma2vue(nr:int,userinfo: UserInfo = None):
  global FIGMA_API_KEY, FILE_KEY
  if(userinfo != None and userinfo.apikey!=None and userinfo.filekey!=None):
    set_variables(userinfo.filekey,userinfo.apikey)
  if(FIGMA_API_KEY=="" and FILE_KEY==""):
    return "Missing token and prototype url!"
  else:
    f = "../tests/prototype"+str(nr)+".json"
    with open(f,"r") as file:
        data = json.load(file)
    convert_prototype(data)
    return "Conversion done!"

@app.get("/download")
def download_file(path: str):
    file_path = f"../output/{path}.zip"
    return FileResponse(
        path=file_path,
        filename=f"{path}.zip",
        media_type="application/zip"
    )
