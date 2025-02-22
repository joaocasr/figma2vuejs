from setup.vueprojectsetup import setup_project, create_project, remove_boilerview, remove_boilercomponents, updateAppVue
from engine.stylegenerator import overwrite_styling
from engine.routergenerator import generate_routes
from engine.pagegenerator import buildpage
from parser.modelconverter import getFigmaData

# extract figma data and build intern model
project_name, pages = getFigmaData()

# project setup
try:
  setup_project(project_name)
  overwrite_styling(project_name)
except Exception as e:
  print(e)

# generate routes to the vue pages
generate_routes(project_name,pages)


# build each page (elements within, styling and components)
for page in pages:
  buildpage(project_name,pages[page])
