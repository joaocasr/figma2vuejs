from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from engine.variantgenerator import writeVariantComponent
from engine.gridgenerator import generateGridTemplate
from engine.pagegenerator import buildpage
from engine.componentgenerator import buildcomponent
from parser.modelconverter import getFigmaData
from parser.model.Melement import Melement
from parser.model.VariantComponent import VariantComponent

import sys

if(len(sys.argv)!=2 and len(sys.argv)!=3):
  print("MANUAL:\n python3 figma2vuejs.py <nrº of prototype>\n python3 figma2vuejs.py <nrº of prototype> <template-file>")
else:
  prototype = sys.argv[1]
  # extract figma data and build intern model
  #try:
  project_name, allpages, orphanComponents, refs, variants = getFigmaData(prototype)
  #except Exception as e:
  #  print(e)
  #  sys.exit()

  # project setup
  try:
    setup_project(project_name)
    overwrite_styling(project_name)
  except Exception as e:
    pass

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
  if(len(sys.argv)==3): mypages = generateGridTemplate(sys.argv[2],allpages)
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


