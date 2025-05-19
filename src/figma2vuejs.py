from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from engine.variantgenerator import writeVariantComponent
from engine.gridgenerator import generateGridTemplate
from engine.pagegenerator import buildpage
from engine.componentgenerator import buildcomponent
from parser.modelconverter import getFigmaData,extractImages,extractSVGs
from parser.model.VariantComponent import VariantComponent

import sys,os,requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
FIGMA_API_KEY = os.environ.get("FIGMA_API_KEY")
FILE_KEY = os.environ.get("FILE_KEY")

headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

if(len(sys.argv)>4 or len(sys.argv)<1):
  print("""****MANUAL****
for conversion using figma api endpoint /files/{id} and prototoype url:
   >  python3 figma2vuejs.py
for conversion using prototoype files:
   >  python3 figma2vuejs.py <nrº of prototype>
for conversion using prototoype files with grid-template:
   >  python3 figma2vuejs.py <nrº of prototype> <nr_row> <nr_column>""")
else:
  prototype = None
  data = None
  if(len(sys.argv)>=2): prototype = sys.argv[1]
  else:
    response = requests.get("https://api.figma.com/v1/files/"+FILE_KEY, headers=headers)
    data = response.json()
  # extract figma data and build intern model
  #try:
  project_name, allpages, orphanComponents, refs, variants = getFigmaData(prototype,data)
  #except Exception as e:
  #  print(e)
  #  sys.exit()

  # project setup
  try:
    setup_project(project_name)
    overwrite_styling(project_name)
  except Exception as e:
    pass

  extractImages(project_name)
  extractSVGs(project_name)

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
    allvariants=[]
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


