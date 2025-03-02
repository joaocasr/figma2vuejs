from parser.model.ContainerElement import ContainerElement
from parser.model.TextElement import TextElement
from parser.model.Mpage import Mpage
from parser.model.Mcomponent import Mcomponent

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
  width = page.containerstyle.width
  height = page.containerstyle.height

  row_height = height / 128

  background = "background-color:white;"
  if(page.containerstyle.backgroundColor!=None):
    background = """\n  background-color:"""+ page.containerstyle.backgroundColor+";\n"
  if(page.containerstyle.background!=None):
    background = """\n  background:"""+ page.containerstyle.background+";\n"
    
  css = """\n.grid-container {
  display:"""+ page.containerstyle.display+ """;
  grid-template-columns:"""+ page.containerstyle.gridtemplatecolumns+""";
  grid-template-rows: repeat(128,minmax("""+ str(row_height) +"""px,1fr));""" + background + """  width: 100%;
  min-height: 100vh;
  max-height: auto;
  margin:"""+ page.containerstyle.margin + """;
  padding:"""+ page.containerstyle.padding + """;
}
  
.grid-item {
  display:flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
  """

  newcsscontent=""
  if page.pagename in font_imports:
    for font in font_imports[page.pagename]:
      newcsscontent += '@import url(' + '"' + font + '");\n'
  newcsscontent += css

  with open("../output/"+name+"/src/assets/"+page.getPagename().lower()+".css","r+") as f:
    lines = f.readlines()  
    lines.insert(0, newcsscontent)
    f.seek(0)   
    f.writelines(lines)

def generateComponentStyle(name,component):

  global font_imports
  pattern = "[:;]"
  idcomponent = re.sub(pattern,"",component.idComponent)

  width = component.style.width
  height = component.style.height

  background = "background-color:white;"
  boxshadow = ""
  border = ""
  if(component.style.backgroundColor!=None): background = """\n  background-color:"""+ component.style.backgroundColor+";"
  if(component.style.background!=None): background = """\n  background:"""+ component.style.background+";"
  if(component.style.boxShadow != None): boxshadow =f"box-shadow: {component.style.boxShadow};"+"\n"
  if(component.style.borderStyle) != None: border =f"border: {component.style.borderStyle};"+"\n"

  css = """\n.component"""+ idcomponent +""" {
  display:"""+ component.style.display+ """;
  grid-template-columns:"""+ component.style.gridtemplatecolumns+""";
  grid-template-rows:"""+ component.style.gridtemplaterows+""";
  grid-column-start:"""+ str(component.style.gridcolumnStart)+""";""" + background + """
  grid-column-end:"""+ str(component.style.gridcolumnEnd)+""";
  grid-row-start:"""+ str(component.style.gridrowStart)+""";"""+ border + boxshadow +"""
  grid-row-end:"""+ str(component.style.gridrowEnd)+""";
  border-radius:"""+ str(component.style.borderRadius) + """px;
  margin:"""+ component.style.margin + """;
  padding:"""+ component.style.padding + """;
}
  
.grid-item {
  display:flex;
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

  with open("../output/"+name+"/src/assets/"+component.componentName.lower()+".css","r+") as f:
    lines = f.readlines()  
    lines.insert(0, newcsscontent)
    f.seek(0)   
    f.writelines(lines)


def generateElemCssProperties(projectname,pagename,cssclass,elem):
  global font_imports
  csskeyvalues = ""
  css = ""
  newline = '\n\t'
  if isinstance(elem,TextElement) : 
    if elem.textStyle.fontStyle != None: csskeyvalues+=f"font-style: {elem.textStyle.fontStyle};{newline}"
    if elem.textStyle.fontWeight != None: csskeyvalues+=f"font-weight: {elem.textStyle.fontWeight};{newline}"
    if elem.textStyle.fontSize != None: csskeyvalues+=f"font-size:{elem.textStyle.fontSize};{newline}"
    if elem.textStyle.fontFamily != None: csskeyvalues+=f"font-family: {elem.textStyle.fontFamily};{newline}"
    if elem.textStyle.color != None: csskeyvalues+=f"color: {elem.textStyle.color};{newline}"
    if elem.textStyle.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.textStyle.gridcolumnStart)};{newline}"
    if elem.textStyle.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.textStyle.gridcolumnEnd)};{newline}"
    if elem.textStyle.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.textStyle.gridrowStart)};{newline}"
    if elem.textStyle.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.textStyle.gridrowEnd)};{newline}"
    csskeyvalues+=f"white-space: nowrap;{newline}"

    font = "//fonts.googleapis.com/css2?family="+elem.textStyle.fontFamily+":wght@"+ str(elem.textStyle.fontWeight) +"&display=swap"
    if((pagename in font_imports) and (font not in font_imports[pagename])):
      font_imports[pagename].append(font)
    if((pagename not in font_imports)):
      font_imports[pagename] = [font]

    css = "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

  if isinstance(elem,ContainerElement): 

    if elem.containerStyle.backgroundColor != None: csskeyvalues+=f"background-color: {elem.containerStyle.backgroundColor};{newline}"
    if elem.containerStyle.background != None: csskeyvalues+=f"background: {elem.containerStyle.background};{newline}"
    if elem.containerStyle.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.containerStyle.boxShadow};{newline}"
    if elem.containerStyle.borderStyle != None: csskeyvalues+=f"border: {elem.containerStyle.borderStyle};{newline}"
    if elem.containerStyle.borderRadius != None: csskeyvalues+=f"border-radius: {elem.containerStyle.borderRadius}px;{newline}"
    if elem.containerStyle.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.containerStyle.gridcolumnStart)};{newline}"
    if elem.containerStyle.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.containerStyle.gridcolumnEnd)};{newline}"
    if elem.containerStyle.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.containerStyle.gridrowStart)};{newline}"
    if elem.containerStyle.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.containerStyle.gridrowEnd)};{newline}"

    if elem.containerStyle.display != None: csskeyvalues+=f"display: {str(elem.containerStyle.display)};{newline}"
    if elem.containerStyle.gridtemplatecolumns != None: csskeyvalues+=f"grid-template-columns: {str(elem.containerStyle.gridtemplatecolumns)};{newline}"
    if elem.containerStyle.gridtemplaterows != None: csskeyvalues+=f"grid-template-rows: {str(elem.containerStyle.gridtemplaterows)};{newline}"

    css = "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

  cssfile = "../output/"+projectname+"/src/assets/"+pagename.lower()+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+pagename.lower()+".css",mode) as f:
    f.write(css)


def calculate_gradientDegree(startPoint,endPoint,color1,color2):
    a = (0,0.5)
    b = (endPoint["x"]-startPoint["x"], endPoint["y"]-startPoint["y"])

    norm_a = math.sqrt(a[0]**2 + a[1]**2) 
    norm_b = math.sqrt(b[0]**2 + b[1]**2) 

    cosalpha = (a[0]*b[0] + a[1]*b[1]) / (norm_a * norm_b)

    x = math.acos(cosalpha)
    degree = x  * (180.0 / math.pi)
    
    rgba1 = (color1["color"]["r"]*255, color1["color"]["g"]*255, color1["color"]["b"]*255, color1["color"]["a"]*255)
    rgba2 = (color2["color"]["r"]*255, color2["color"]["g"]*255, color2["color"]["b"]*255, color2["color"]["a"]*255)

    lineargradient = "linear-gradient("+str(degree)+"deg, " + "rgba("+','.join(str(val) for val in rgba1)+"), " + "rgba("+','.join(str(val) for val in rgba2)+"))" 
    return lineargradient