from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from engine.pagegenerator import buildpage
from engine.componentgenerator import buildcomponent
from parser.modelconverter import getFigmaData

import sys

if(len(sys.argv)!=2):
  print("man: python3 figma2vuejs.py <nrº of prototype>")
else:
  prototype = sys.argv[1]
  # extract figma data and build intern model
  project_name, pages, allpages = getFigmaData(prototype)

  # project setup
  try:
    setup_project(project_name)
    overwrite_styling(project_name)
  except Exception as e:
    pass

  # generate routes to the vue pages
  generate_routes(project_name,pages)

  # pages_info will be a dictionary of the path and components ids of each page
  pagesInfo = dict()
  for page in allpages:
    pagesInfo[page] = {"path":allpages[page].pagepath, "name": page, "id": allpages[page].idpage, "components": allpages[page].components}

  # filter unique components by its id
  uniqueComponents = []
  for page in pagesInfo:
    for x in pagesInfo[page]["components"]:
      if(not any(x.idComponent == c.idComponent for c in uniqueComponents)):
        uniqueComponents.append(x)

  for component in uniqueComponents:
    buildcomponent(component,project_name,pagesInfo)
  
  # build each page (elements within, styling and components)
  for page in pages:
    buildpage(project_name,pages[page],pagesInfo)
