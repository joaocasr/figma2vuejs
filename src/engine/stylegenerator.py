from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement
from parser.model.VectorElement import VectorElement
from parser.model.TextElement import TextElement
from parser.model.Mpage import Mpage
from parser.model.Mcomponent import Mcomponent
from utils.processing import getFormatedName,getElemId

import os
import re
import math

# key: page_name; value: list_of_font_imports -> list(string)
font_imports = {}

def overwrite_styling(name):
    print("Updating global css properties...")
    maincss="""@import './base.css';


@media (min-width: 1024px) {
  #app {
      padding: 0;
  }
}
"""
    filemain = "../output/"+name+"/src/assets/main.css"
    if os.path.isfile(filemain):
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
  margin:0px;
}
"""
    else:
        raise Exception("main.css file not found!")
    filebase = "../output/"+name+"/src/assets/base.css"
    if os.path.isfile(filebase):
        f= open(filebase,"w")
        f.write(basecss)
        f.close()
    else:
        raise Exception("base.css file not found!")


def generatePageStyle(name,page):
  global font_imports
  width = page.style.width
  height = page.style.height

  row_height = max(height / 128, 8)

  background = "background-color:rgba(0,0,0,0);"
  if(page.style.backgroundColor!=None):
    background = """\n  background-color:"""+ page.style.backgroundColor+";\n"
  if(page.style.background!=None):
    background = """\n  background:"""+ page.style.background+";\n"

  gridtemplaterows = f"repeat(128, {str(row_height)}px);"+"\n"
  #gridtemplaterows = f"repeat(128,minmax("+ str(row_height) +"px,1fr));"
  if(page.style.getGridTemplateArea()!=None):
    gridtemplaterows = page.style.getGridTemplateRows() + ";\n"
    
  cssgridcontainer = """\n.grid-container {
  display:"""+ page.style.display+ """;
  grid-template-columns:"""+ page.style.gridtemplatecolumns+""";
  grid-template-rows:""" + gridtemplaterows + background + """  width: 100%;
  min-height: 100vh;
  max-height: auto;
  margin:"""+ page.style.margin + """;
  padding:"""+ page.style.padding + """;
  """
  #  gap:10px;
  if(page.style.getGridTemplateArea()!=None):
    cssgridcontainer+="grid-template-areas:\n    "+ '\n    '.join(page.style.getGridTemplateArea())+";\n  gap: "+page.style.getGap()+";\n"

  cssgriditem = """}
 
.grid-item {
  display:flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
  """

  css = cssgridcontainer + cssgriditem
  newcsscontent= ""
  if page.pagename in font_imports:
    for font in font_imports[page.pagename]:
      newcsscontent += '@import url(' + '"' + font + '");\n'
  newcsscontent += css

  cssfile="../output/"+name+"/src/assets/"+getFormatedName(page.getPagename().lower())+".css"
  if not os.path.isfile(cssfile):
    with open(cssfile,"w") as f:
      f.write(newcsscontent)
  else:
    with open("../output/"+name+"/src/assets/"+getFormatedName(page.getPagename().lower())+".css","r+") as f:
      lines = f.readlines()  
      lines.insert(0, newcsscontent)
      f.seek(0)   
      f.writelines(lines)

def generateComponentStyle(name,component):
  global font_imports
  idcomponent = getElemId(component.idComponent)

  width = component.style.width
  height = component.style.height
  background = "background-color:rgba(0,0,0,0);"
  if(component.style.backgroundColor!=None):
    background = """\n  background-color:"""+ component.style.backgroundColor+";\n"
  if(component.style.background!=None):
    background = """\n  background:"""+ component.style.background+";\n"

  boxshadow = ""
  border = ""
  borderRadius=""
  zindex=""
  if(component.style.background!=None): background = """\n  background:"""+ component.style.background+";"
  if(component.style.boxShadow != None): boxshadow ="\n  "+f"box-shadow: {component.style.boxShadow};"
  if(component.style.borderStyle) != None: border ="\n  "+f"border: {component.style.borderStyle};"
  if(component.style.borderRadius) != None: borderRadius ="\n  "+f"border-radius: {component.style.borderRadius}px;"
  if(component.getzindex()>0): zindex = "\n  "+f"z-index: "+str(component.getzindex())

  css = """\n.component"""+ idcomponent +""" {
  display:"""+ component.style.display+ """;
  grid-template-columns:"""+ component.style.gridtemplatecolumns+""";
  grid-template-rows:"""+ component.style.gridtemplaterows+""";
  grid-column-start:"""+ str(component.style.gridcolumnStart)+""";
  grid-column-end:"""+ str(component.style.gridcolumnEnd)+""";
  grid-row-start:"""+ str(component.style.gridrowStart)+""";
  grid-row-end:"""+ str(component.style.gridrowEnd)+""";
  margin:"""+ component.style.margin + """;
  padding:"""+ component.style.padding + """;"""+ border + boxshadow + background + borderRadius + zindex + """
}
  
.grid-item-"""+ idcomponent + """ {
  text-align: center;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
  """
  newcsscontent=""
  if component.componentName in font_imports:
    for font in font_imports[component.componentName]:
      newcsscontent += '@import url(' + '"' + font + '");\n'
  newcsscontent += css
  cssfile="../output/"+name+"/src/assets/"+getFormatedName(component.componentName.lower())+".css"
  if not os.path.isfile(cssfile):
    with open(cssfile,"w") as f:
      f.write(newcsscontent)
  else:
    with open(cssfile,"r+") as f:
      lines = f.readlines()  
      lines.insert(0, newcsscontent)
      f.seek(0)   
      f.writelines(lines)

def generatePaginatorCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
}
  :deep(."""+ str(cssclass) + """ .v-pagination__item--is-active .v-btn) {
    background-color:  """+  str(elem.style.getbackgroundColor()) +""" !important;
    color: """+  str(elem.style.getcolor()) +""" !important;
    border-radius:"""+  str(elem.style.getborderRadius()) +"""px;
  }

  :deep(."""+ str(cssclass) + """ .v-pagination__item .v-btn) {
    color:  """+  str(elem.style.getcolor()) +""";
  }

  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateFormCssProperties(projectname,pagename,cssclass,elem,formclass,inputclass,btnclass):
  css ="""\n."""+ str(formclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  }
 
  ."""+ str(btnclass) + """ {
    background-color: """+  str(elem.style.getbackgroundcolorbtn())+""";
    border-radius: 8px;
    width:200px;
    height:50px;
    margin-top: 10px;
    position: relative;
    left:  """+  str(elem.style.getwidthinput()/4)+"""px;
  }
."""+ str(inputclass) + """ .p-inputtext{ 
  --p-inputtext-background:"""+  str(elem.style.getbackgroundcolor())+""";
  width: """+  str(elem.style.getwidthinput())+"""px;
  color: """+  str(elem.style.getinputColor())+""";
}
"""
  if(elem.style.getlabeltextSize()!=None and elem.style.getlabeltextColor()!=None):
    css+=""".label"""+ str(cssclass) + """{
  font-size: """+  str(elem.style.getlabeltextSize())+"""px;
  color: """+  str(elem.style.getlabeltextColor())+""";
}
    """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateCheckboxCssProperties(projectname,pagename,cssclass,labelclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
    margin:5px;
    --p-checkbox-background:  """+  str(elem.style.getColorBackground())+""";
    --p-checkbox-border-radius:"""+ str(elem.style.getboxRadius()/2)+"""px;
  }

  ."""+ str(labelclass) + """ {
    color: """+  str(elem.style.getColortxt())+""";
    margin-left: 5px;
    position: relative;
    top:3px;
  }
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateVideoCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  }
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateMenuCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  }
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def setComponentPositionCSS(projectname,pagename,componentName,elem):
  top="0%"
  left="0%"
  if(elem.style.gridrowStart>=2):
    top = str(round(elem.style.gridrowStart/128)*100)+"%"
  if(elem.style.gridcolumnStart>=2):
    left = str(round(elem.style.gridcolumnStart/64)*100)+"%"
  css ="""\n."""+ str(componentName) + """ {
  position:"""+  str(elem.style.getPosition()) +""";
  top:"""+ top +""";
  left:"""+ left +""";
  z-index: 5;
}
"""
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateVueSelectCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
}

div:deep(."""+ str(cssclass) + """ .v-input__control) {
  display: flex;
  grid-area: control;
  min-width: 300px;
  background-color:"""+  str(elem.style.background_color)+""";
  color: """+ str(elem.style.placeholder_color) +""";
  border-radius: """+ str(elem.style.getborderRadius()) +"""px;
}

div:deep(."""+ str(cssclass) + """ .v-field__outline) {
  --v-field-border-width:0px;
  --v-field-border-opacity:0;
}

  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateInputSearchFilterCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    position: relative;  
    display: flex;       
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
}
."""+ str(cssclass) + """ .p-inputtext{
   --p-inputtext-background: rgba("""+  str(elem.style.getbackgroundcolor())+""");
   --p-inputtext-color: rgba("""+  str(elem.style.getcolor())+""");
   --p-inputtext-border-radius:"""+  str(elem.style.getborderradius())+"""px;
    padding-left: 35px; 
}

\n."""+ str(cssclass) + """ .pi {
  position: absolute;
  left: 10px;
  transform: translateY(10%);
  pointer-events: none;
}
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateSliderCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
    --p-slider-track-background:  """+  str(elem.style.getbackgroundtrack())+""";
}

div:deep(."""+str(cssclass)+""" .p-slider-range){
    --p-slider-range-background:  """+ str(elem.style.getbackgroundcontent()) +""";
}
 
div:deep(."""+str(cssclass)+""" .p-slider-handle){
    --p-slider-handle-content-background:  """+  str(elem.style.getbackgroundcontent()) +""";
    --p-slider-handle-content-hover-background: """+  str(elem.style.getcolorhover()) +""";
}
"""
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateTableCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
    --p-datatable-row-background: """+  str(elem.style.getbackgroundBody())+""";
    --p-datatable-body-cell-border-color: """+  str(elem.style.getbackgroundBody())+""";
    --p-datatable-row-color: """+  str(elem.style.gettextColor())+""";
}
:deep(."""+str(cssclass)+""" .p-datatable-header-cell){
  background:"""+  str(elem.style.getbackgroundHeader())+""";
  color:""" +  str(elem.style.getheadertextColor())+""";
}

"""
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateRatingCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
	  color: """+  str(elem.style.getstarColor())+""";
}
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateDatePickerCssProperties(projectname,pagename,cssclass,elem):
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
}

:deep(."""+str(cssclass)+""" .p-datepicker-input){
	background-color: """+  str(elem.style.getbackgroundcolor())+""";
}
 
 :deep(."""+str(cssclass)+""" .p-datepicker-dropdown .p-icon){
	color: """+  str(elem.style.geticonrgbacolor())+""";
}

:deep(."""+str(cssclass)+""" .p-datepicker-dropdown){
	background-color:"""+  str(elem.style.getdropdownbackgroundcolor())+""";
}
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateScrollCSS(projectname,pagename,cssclass,elem):
  if(elem.style.getOverflowDirection()=="HORIZONTAL"):
    css=""".scroll-wrapper"""+ str(cssclass) +""" {
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap;
    cursor: grab;
    user-select: none;
  	display: flex;
    overflow: auto;
    width: """+  str(elem.style.width) +"""px;
    height: """+  str(elem.style.height) +"""px;
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  }

  .scroll-wrapper"""+ str(cssclass) +""".active {
    cursor: grabbing;
  }
"""
  if(elem.style.getOverflowDirection()=="VERTICAL"):
    css=""".scroll-wrapper"""+ str(cssclass) +""" {
    overflow-x: hidden;
    overflow-y: auto;
    white-space: nowrap;
    cursor: grab;
  	display: block;
    overflow: auto;
    user-select: none;
    width: """+  str(elem.style.width) +"""px;
    height: """+  str(elem.style.height) +"""px;
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  }

  .scroll-wrapper"""+ str(cssclass) +""".active {
    cursor: grabbing;
  }
"""
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateShapeCSS(projectname,pagename,cssclass,type,elem):
  clippath=""
  if(type=="STAR"):
    clippath = "polygon(50% 0,79% 90%,2% 35%,98% 35%,21% 90%)"
  if(type=="REGULAR_POLYGON"):
    clippath = "polygon(50% 0,100% 100%,0 100%)"
  if(type=="RECTANGLE"):
    clippath = "polygon(0 0, 0% 100%, 100% 100%,100% 0)"
  if(type=="ELLIPSE" and abs(int(elem.style.width)-int(elem.style.height))<5):
    clippath = "circle(50% at 50% 50%)"
  if(type=="ELLIPSE" and abs(int(elem.style.width)-int(elem.style.height))>=5):
    clippath = "ellipse(50% 30% at 50% 50%)"
  css=""
  css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
    grid-template-columns:"""+ str(elem.style.gridtemplatecolumns)+""";
    grid-template-rows:"""+ str(elem.style.gridtemplaterows)+""";
    aspect-ratio: 1;
    clip-path: """+  str(clippath)+ """;
    """
  css+="""height: """+  str(elem.style.height) + """px;
    width: """+  str(elem.style.width) + """px;"""

  if(type=="LINE"):
    css ="""\n."""+ str(cssclass) + """ {
    grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
    grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
    grid-row-start: """+  str(elem.style.gridrowStart)+""";
    grid-row-end: """+  str(elem.style.gridrowEnd)+""";
    background: """+  str(elem.style.background)+""";
    height: 1px;
    border: 0;
    padding: 0;
    """
  if(elem.style.getBackground()!=None): css+="background:"+elem.style.getBackground()+";\n\t"
  if(elem.style.getBackgroundColor()!=None): css+="background-color:"+elem.style.getBackgroundColor()+";\n\t"
  if(elem.style.getborderRadius()!=None): css+="border-radius:"+elem.style.getborderRadius()+"px;\n\t"
  if(elem.style.transform!=None): css+="transform: rotate("+elem.style.getTransform()+");\n\t"
  if(elem.style.getBorderTopLeftRadius() != None and elem.style.getBorderTopLeftRadius()!="0.0"): css+=f"border-top-left-radius: {elem.style.getBorderTopLeftRadius()}px;"+'\n\t'
  if(elem.style.getBorderTopRightRadius() != None and elem.style.getBorderTopRightRadius()!="0.0"): css+=f"border-top-right-radius: {elem.style.getBorderTopRightRadius()}px;"+'\n\t'
  if(elem.style.getBorderBottomLeftRadius() != None and elem.style.getBorderBottomLeftRadius()!="0.0"): css+=f"border-bottom-left-radius: {elem.style.getBorderBottomLeftRadius()}px;"+'\n\t'
  if(elem.style.getBorderBottomRightRadius() != None and elem.style.getBorderBottomRightRadius()!="0.0"): css+=f"border-bottom-right-radius: {elem.style.getBorderBottomRightRadius()}px;"+'\n\t'
  if(elem.style.getDisplay() != None):
    css+=f"display: {elem.style.getDisplay()};"+'\n\t'
  else:
    css+=f"display: block;"+'\n\t'
  if(elem.style.getOpacity() != None): css+=f"opacity: {elem.style.getOpacity()};"+'\n\t'
  if(elem.style.getBorderColor()!=None):
    css+="    border: solid;\n"+'    '+ f"border-color: {elem.style.getBorderColor()};"+'    '+ f"border-radius: {elem.style.getborderRadius()}px;"+'    '+ f"border-width: {elem.style.getborderWidth()}px;"+'\n'
  css = css + "}"
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateShapeShadowCSS(projectname,pagename,cssclass,elem):
  css ="""\n."""+ cssclass + """ {
  grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
  grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
  grid-row-start: """+  str(elem.style.gridrowStart)+""";
  grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  filter: drop-shadow("""+  str(elem.style.getBoxShadow())+""");
}
  """
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)

def generateElemCssProperties(projectname,pagename,cssclass,elem):
  global font_imports
  csskeyvalues = ""
  css = ""
  newline = '\n\t'
  if isinstance(elem,TextElement) : 
    if elem.style.fontStyle != None: csskeyvalues+=f"font-style: {elem.style.fontStyle};{newline}"
    if elem.style.fontWeight != None: csskeyvalues+=f"font-weight: {elem.style.fontWeight};{newline}"
    if elem.style.fontSize != None: csskeyvalues+=f"font-size: {elem.style.fontSize};{newline}"
    if elem.style.opacity != None: csskeyvalues+=f"opacity: {elem.style.opacity};{newline}"
    if elem.style.fontFamily != None: csskeyvalues+=f"font-family: {elem.style.fontFamily};{newline}"
    if elem.style.textHorizontalAlign != None: csskeyvalues+=f"text-align: {elem.style.textHorizontalAlign.lower()};{newline}"
    if elem.style.lineHeight != None: csskeyvalues+=f"line-height: {str(elem.style.lineHeight)};{newline}"
    if elem.style.color != None: csskeyvalues+=f"color: {elem.style.color};{newline}"
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    if(elem.style.getOpacity() != None): csskeyvalues+=f"opacity: {elem.style.getOpacity()};{newline}"
    if elem.style.display != None:
      csskeyvalues+=f"display: {str(elem.style.display)};{newline}"
    else:
      csskeyvalues+=f"display: flex;{newline}"
    csskeyvalues+=f"overflow-wrap: break-word;{newline}" #word-break: break-word;{newline}

    if(elem.style.textAutoResize == "WIDTH_AND_HEIGHT"):
      csskeyvalues+=f"white-space: normal;{newline}"
    elif(elem.style.textAutoResize == "WIDTH"):
      csskeyvalues+=f"white-space: nowrap;{newline}"
    elif(elem.style.textAutoResize == "HEIGHT"):
      csskeyvalues+=f"word-wrap: break-word;{newline}"

    alignment = "stretch"
    if(elem.style.textHorizontalAlign.lower()=="center"): alignment = "center"
    csskeyvalues +=f"width: 100%;{newline}align-items: {alignment};{newline}justify-content: stretch;{newline}"
    #height:auto
    font = "https://fonts.googleapis.com/css2?family="+elem.style.fontFamily+":wght@"+ str(elem.style.fontWeight) +"&display=swap"
    if((pagename in font_imports) and (font not in font_imports[pagename])):
      font_imports[pagename].append(font)
    elif((pagename not in font_imports)):
      font_imports[pagename] = [font]
    css = "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

  if isinstance(elem,ImageElement) : 
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    if elem.style.getCornerRadius() != None: csskeyvalues+=f"border-radius: {elem.style.getCornerRadius()}px;{newline}"
    if elem.style.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.style.boxShadow};{newline}"
    if(elem.style.getBorderTopLeftRadius() != None and elem.style.getBorderTopLeftRadius()!="0.0"): csskeyvalues+=f"border-top-left-radius: {elem.style.getBorderTopLeftRadius()}px;{newline}"
    if(elem.style.getBorderTopRightRadius() != None and elem.style.getBorderTopRightRadius()!="0.0"): csskeyvalues+=f"border-top-right-radius: {elem.style.getBorderTopRightRadius()}px;{newline}"
    if(elem.style.getBorderBottomLeftRadius() != None and elem.style.getBorderBottomLeftRadius()!="0.0"): csskeyvalues+=f"border-bottom-left-radius: {elem.style.getBorderBottomLeftRadius()}px;{newline}"
    if(elem.style.getBorderBottomRightRadius() != None and elem.style.getBorderBottomRightRadius()!="0.0"): csskeyvalues+=f"border-bottom-right-radius: {elem.style.getBorderBottomRightRadius()}px;{newline}"

    #if(elem.style.gridcolumnEnd-elem.style.gridcolumnStart>60 or elem.style.gridrowEnd-elem.style.gridrowStart>60): csskeyvalues +=f"width: 100%;{newline}height: 100%;{newline}display: block;{newline}object-fit: cover;{newline}"

    css = "."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

  if isinstance(elem,VectorElement) : 
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    if elem.style.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.style.boxShadow};{newline}"
    #if(elem.style.gridcolumnEnd-elem.style.gridcolumnStart>60 or elem.style.gridrowEnd-elem.style.gridrowStart>60): csskeyvalues +=f"width: 100%;{newline}height: 100%;{newline}display: block;{newline}object-fit: cover;{newline}"

    css = "."+cssclass+" {\n\t"+"min-width: 100%;\n\tmin-height: 100%;"+ csskeyvalues[:-1] +"}\n\n"
  
  if isinstance(elem,ContainerElement): 
    if(elem.style.gridrowStart==None and elem.style.gridrowEnd==None and elem.style.getHeight()!=None):
      csskeyvalues+=f"height: {elem.style.getHeight()}px;{newline}"
  
    if elem.style.backgroundColor != None: csskeyvalues+=f"background-color: {elem.style.backgroundColor};{newline}"
    if elem.style.background != None: csskeyvalues+=f"background: {elem.style.background};{newline}"
    if elem.style.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.style.boxShadow};{newline}"
    if elem.style.margin != None: csskeyvalues+=f"margin: {elem.style.margin};{newline}"
    if elem.style.borderStyle != None: csskeyvalues+=f"border: {elem.style.borderStyle};{newline}"
    if elem.style.borderRadius != None: csskeyvalues+=f"border-radius: {elem.style.borderRadius}px;{newline}"
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    if(elem.style.getMarginLeft() != None): csskeyvalues+=f"margin-left: {str(elem.style.getMarginLeft())};{newline}"
    if(elem.style.getBorderTopLeftRadius() != None and elem.style.getBorderTopLeftRadius()!="0.0"): csskeyvalues+=f"border-top-left-radius: {elem.style.getBorderTopLeftRadius()}px;{newline}"
    if(elem.style.getBorderTopRightRadius() != None and elem.style.getBorderTopRightRadius()!="0.0"): csskeyvalues+=f"border-top-right-radius: {elem.style.getBorderTopRightRadius()}px;{newline}"
    if(elem.style.getBorderBottomLeftRadius() != None and elem.style.getBorderBottomLeftRadius()!="0.0"): csskeyvalues+=f"border-bottom-left-radius: {elem.style.getBorderBottomLeftRadius()}px;{newline}"
    if(elem.style.getBorderBottomRightRadius() != None and elem.style.getBorderBottomRightRadius()!="0.0"): csskeyvalues+=f"border-bottom-right-radius: {elem.style.getBorderBottomRightRadius()}px;{newline}"
    if(elem.style.getMinHeight() != None): csskeyvalues+=f"min-height: {elem.style.getMinHeight()}px;{newline}"
    if(elem.style.getMinWidth() != None): csskeyvalues+=f"min-width: {elem.style.getMinWidth()}px;{newline}"
    if(elem.style.getPosition() != None): csskeyvalues+=f"position: {elem.style.getPosition()};{newline}"

    if(elem.getinitialOpacity()!=None): csskeyvalues+=f"opacity: {str(elem.getinitialOpacity())};{newline}"
    if elem.style.display != None: csskeyvalues+=f"display: {str(elem.style.display)};{newline}"
    if elem.style.gridtemplatecolumns != None: csskeyvalues+=f"grid-template-columns: {str(elem.style.gridtemplatecolumns)};{newline}"
    if elem.style.gridtemplaterows != None: csskeyvalues+=f"grid-template-rows: {str(elem.style.gridtemplaterows)};{newline}"
    csskeyvalues +=f"padding: 0;{newline}"
    gridareacss = ""
    if(elem.style.getgridArea()!=None):
      gridareacss = "#"+elem.name.lower()+" {\n\t"+ "grid-area:"+elem.style.getgridArea()+";\n}\n\n"

    hover=""
    if(elem.style.gethashoverProperty()==True):
      hover="\n."+cssclass+":hover {\n\t"+ "opacity:"+str(elem.style.getOpacity())+";\n}\n"
    css = gridareacss + "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"
    css+=hover
    
  cssfile = "../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+getFormatedName(pagename.lower())+".css",mode) as f:
    f.write(css)


def calculate_lineargradientDegree(points,colors):
  startPoint = points[1]
  endPoint = points[0]
  a = (endPoint["x"]-startPoint["x"],0)
  b = (endPoint["x"]-startPoint["x"],endPoint["y"]-startPoint["y"])
  lineargradient = "linear-gradient("
  scolors = ""
  norm_a = math.sqrt(a[0]**2 + a[1]**2) 
  norm_b = math.sqrt(b[0]**2 + b[1]**2) 
  print(a)
  print(b)
  cosalpha = (a[0]*b[0] + a[1]*b[1]) / (norm_a * norm_b)
  x = math.acos(cosalpha)
  degree = ((x * 180)/math.pi)  + 90
  print(degree)
  if(b[1]>a[1]): degree-=180
  for c in colors:
    rgba = (c["color"]["r"]*255, c["color"]["g"]*255, c["color"]["b"]*255, c["color"]["a"]*255)
    scolors+="rgba("+','.join(str(val) for val in rgba)+") "+ str(round(c["position"]*100))+"%, "
  lineargradient += str(degree)+"deg, " + scolors[:-2] + ")"
  return lineargradient

def calculate_radialgradientDegree(points,colors):
  center = (points[0]["x"],points[0]["y"])
  angle = f"50% 50% at {center[0]*100}% {center[1]*100}%, "
  radialgradient = "radial-gradient("+angle
  for c in colors:
    rgba = (c["color"]["r"]*255, c["color"]["g"]*255, c["color"]["b"]*255, c["color"]["a"]*255)
    radialgradient += "rgba("+','.join(str(val) for val in rgba)+")"+ " "+ str(c["position"]*100)+"%, "
    
  radialgradient=radialgradient[:-2]
  radialgradient+=");"
  return radialgradient

def calculate_angulargradientDegree(points,colors):
  a = (0,0.5)
  startPoint = points[1]
  endPoint = points[0]
  b = (endPoint["x"]-startPoint["x"], endPoint["y"]-startPoint["y"])
  norm_a = math.sqrt(a[0]**2 + a[1]**2) 
  norm_b = math.sqrt(b[0]**2 + b[1]**2) 

  cosalpha = (a[0]*b[0] + a[1]*b[1]) / (norm_a * norm_b)

  x = math.acos(cosalpha)
  degree = math.degrees(x)
  if(degree<0): degree+=360
  center = (points[0]["x"]*100,points[0]["y"]*100)
  angle = "from "+str(degree)+f"deg at {center[0]}% {center[1]}%, "
  ipoint = 0
  angulargradient = "conic-gradient("+angle
  for c in colors:
    rgba = (c["color"]["r"]*255, c["color"]["g"]*255, c["color"]["b"]*255, c["color"]["a"]*255)

    angulargradient += "rgba("+','.join(str(val) for val in rgba)+"), "
    ipoint+=1
  angulargradient=angulargradient[:-2]
  angulargradient+=");"
  return angulargradient
