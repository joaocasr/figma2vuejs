from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement
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
  width = page.style.width
  height = page.style.height

  row_height = max(height / 128, 8)

  background = "background-color:white;"
  if(page.style.backgroundColor!=None):
    background = """\n  background-color:"""+ page.style.backgroundColor+";\n"
  if(page.style.background!=None):
    background = """\n  background:"""+ page.style.background+";\n"

  gridtemplaterows = f"repeat(128, {str(row_height)}px);"+"\n"
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
  if(component.style.boxShadow != None): boxshadow ="\n  "+f"box-shadow: {component.style.boxShadow};"
  if(component.style.borderStyle) != None: border ="\n  "+f"border: {component.style.borderStyle};"

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


  css ="""\n."""+ cssclass + """ {
  grid-column-start: """+  str(elem.style.gridcolumnStart) +""";
  grid-column-end: """+  str(elem.style.gridcolumnEnd)+""";
  grid-row-start: """+  str(elem.style.gridrowStart)+""";
  grid-row-end: """+  str(elem.style.gridrowEnd)+""";
  aspect-ratio: 1;
  background: """+  elem.style.background+""";
  clip-path: """+  clippath+ """;
  height: """+  str(elem.style.height) + """px;
  width:  """+  str(elem.style.width) + """px;
  """
  if(elem.style.transform!=None): css+="transform: rotate("+elem.style.getTransform()+");\n"

  css = css + "}"
  cssfile = "../output/"+projectname+"/src/assets/"+pagename.lower()+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+pagename.lower()+".css",mode) as f:
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
  cssfile = "../output/"+projectname+"/src/assets/"+pagename.lower()+".css"
  mode = "w"
  if os.path.isfile(cssfile):
    mode = "a"
  with open("../output/"+projectname+"/src/assets/"+pagename.lower()+".css",mode) as f:
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
    if elem.style.fontFamily != None: csskeyvalues+=f"font-family: {elem.style.fontFamily};{newline}"
    if elem.style.textHorizontalAlign != None: csskeyvalues+=f"text-align: {elem.style.textHorizontalAlign.lower()};{newline}"
    if elem.style.lineHeight != None: csskeyvalues+=f"line-height: {str(elem.style.lineHeight)};{newline}"
    if elem.style.color != None: csskeyvalues+=f"color: {elem.style.color};{newline}"
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    csskeyvalues+=f"overflow-wrap: break-word;{newline}" #word-break: break-word;{newline}

    if(elem.style.textAutoResize == "WIDTH_AND_HEIGHT"):
      csskeyvalues+=f"white-space: normal;{newline}"
    elif(elem.style.textAutoResize == "WIDTH"):
      csskeyvalues+=f"white-space: nowrap;{newline}"
    elif(elem.style.textAutoResize == "HEIGHT"):
      csskeyvalues+=f"word-wrap: break-word;{newline}"

    alignment = "stretch"
    if(elem.style.textHorizontalAlign.lower()=="center"): alignment = "center"
    csskeyvalues +=f"width: 100%;{newline}display: flex;{newline}align-items: {alignment};{newline}justify-content: stretch;{newline}"
    #height:auto

    font = "//fonts.googleapis.com/css2?family="+elem.style.fontFamily+":wght@"+ str(elem.style.fontWeight) +"&display=swap"
    if((pagename in font_imports) and (font not in font_imports[pagename])):
      font_imports[pagename].append(font)
    if((pagename not in font_imports)):
      font_imports[pagename] = [font]

    css = "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

  if isinstance(elem,ImageElement) : 
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"
    if elem.style.getCornerRadius() != None: csskeyvalues+=f"border-radius: {elem.style.getCornerRadius()}px;{newline}"
    if elem.style.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.style.boxShadow};{newline}"

    css = "."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"
  
  if isinstance(elem,ContainerElement): 

    if elem.style.backgroundColor != None: csskeyvalues+=f"background-color: {elem.style.backgroundColor};{newline}"
    if elem.style.background != None: csskeyvalues+=f"background: {elem.style.background};{newline}"
    if elem.style.boxShadow != None: csskeyvalues+=f"box-shadow: {elem.style.boxShadow};{newline}"
    if elem.style.borderStyle != None: csskeyvalues+=f"border: {elem.style.borderStyle};{newline}"
    if elem.style.borderRadius != None: csskeyvalues+=f"border-radius: {elem.style.borderRadius}px;{newline}"
    if elem.style.gridcolumnStart != None: csskeyvalues+=f"grid-column-start: {str(elem.style.gridcolumnStart)};{newline}"
    if elem.style.gridcolumnEnd != None: csskeyvalues+=f"grid-column-end: {str(elem.style.gridcolumnEnd)};{newline}"
    if elem.style.gridrowStart != None: csskeyvalues+=f"grid-row-start: {str(elem.style.gridrowStart)};{newline}"
    if elem.style.gridrowEnd != None: csskeyvalues+=f"grid-row-end: {str(elem.style.gridrowEnd)};{newline}"

    if elem.style.display != None: csskeyvalues+=f"display: {str(elem.style.display)};{newline}"
    if elem.style.gridtemplatecolumns != None: csskeyvalues+=f"grid-template-columns: {str(elem.style.gridtemplatecolumns)};{newline}"
    if elem.style.gridtemplaterows != None: csskeyvalues+=f"grid-template-rows: {str(elem.style.gridtemplaterows)};{newline}"
    csskeyvalues +=f"padding: 0;{newline}"
    gridareacss = ""
    if(elem.style.getgridArea()!=None):
      gridareacss = "#"+elem.name.lower()+" {\n\t"+ "grid-area:"+elem.style.getgridArea()+";\n}\n\n"

    css = gridareacss + "\n."+cssclass+" {\n\t"+ csskeyvalues[:-1] +"}\n\n"

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