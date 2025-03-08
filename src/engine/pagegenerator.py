from engine.stylegenerator import generatePageStyle, generateElemCssProperties, generateShapeCSS
from engine.logicgenerator import handleBehaviour
from parser.model.Mcomponent import Mcomponent
from parser.model.TextElement import TextElement
from parser.model.ShapeElement import ShapeElement
from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement

import xml.etree.ElementTree as ET
from lxml import etree, html
import re

allhooks = dict()
imports = dict()
components = dict()
allPagesInfo = dict()

def buildpage(name,page,pagesInfo):
    global allhooks,imports,components,allPagesInfo
    #setup a page
    allhooks[page.pagename] = {}
    imports[page.pagename] = []
    components[page.pagename] = []
    allPagesInfo = pagesInfo
    output = ""  
    for element in page.elements:
        output += processChildren(element,name,page.pagename)

    writeVue(name,page,output)

def processChildren(data,projectname,pagename):
    if(data==None): return ""
    if(len(data.children)>0):
        content=""
        output, endtag = applytransformation(data,projectname,pagename)
        for element in data.children:
            content += processChildren(element,projectname,pagename)

        return output + content + endtag

    else:
        output, endtag = applytransformation(data,projectname,pagename)
        output += endtag    
        return output

# Do a better handling of the tags
def applytransformation(elem,projectname,pagename):
    global allPagesInfo, allhooks, components
    cssclass = ""
    pattern = "[:;]"
    if(not isinstance(elem,Mcomponent)): cssclass = re.sub(pattern,"",elem.idElement)
    else: cssclass = re.sub(pattern,"",elem.idComponent)
    
    # insert directives and functions if there is some behaviour
    directives, hooks = handleBehaviour(elem,allPagesInfo)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[pagename].setdefault(hook, []).extend(hooks[hook])
    id = ""
    if(elem.style.getgridArea()!=None):
        id = ' id="'+elem.style.getgridArea()+'"'
    if(isinstance(elem, TextElement) and (elem.tag=="" or elem.tag == None)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)

        txt = re.sub(r"\n", "<br/>",elem.text)
        return ("<p class="+'"grid-item text'+ cssclass  + '" '+ ' '.join(d for d in directives) +">"+txt, "</p>")
    if(isinstance(elem, ContainerElement) and (elem.tag=="" or elem.tag == None)):

        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)

        return ("<div"+ id +" class="+'"grid-item container'+ cssclass + '" '+ ' '.join(d for d in directives) +">", "</div>")
    if(isinstance(elem, ImageElement) and elem.tag=="img"):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)

        return ("<img"+ id +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getSrc() + '"' + ' '.join(d for d in directives) , "/>")
    if(isinstance(elem, ShapeElement)):
        cssclassifier = ""
        cssclassifier = elem.getType().lower() + str(cssclass)
        generateShapeCSS(projectname,pagename,cssclassifier,elem.getType(),elem)

        return ("<div"+ id +" class="+'"grid-item '+ cssclassifier + '" '+ ' '.join(d for d in directives) +">", "</div>")
    if isinstance(elem, Mcomponent):
        componentName = elem.componentName.capitalize()
        components.setdefault(pagename, []).append(elem.componentName)
        return ("<"+componentName+">","</"+componentName+">")
    return ("","")

def writeVue(name,page,content):
    global allhooks, components 
    componentsimports=""
    for comp in components[page.getPagename()]:
        componentsimports += "import "+str(comp).capitalize()+" from '@/components/"+str(comp).capitalize()+".vue';\n" 
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    template = '<div class="grid-container">'+ content + '</div>'
    pagehooks=""
    pagecomponents="""\n    components:{\n        """+ ',\n        '.join(components[page.getPagename()]).capitalize() +"""\n    },"""
    for hook in allhooks[page.getPagename()]:
        pagehooks = hook + ":{\n"
        for content in allhooks[page.getPagename()][hook]:
            pagehooks += content[1] + ",\n"
        pagehooks = pagehooks[:-2]
        pagehooks +="\n\t}"
    if(len(pagehooks)>0): pagehooks= ",\n    "+pagehooks
    vuepage = """<template>\n""" + processTemplate(template,page.getPagename()) + """
</template>

<script>
"""+ componentsimports +"""
export default {"""+ pagecomponents +"""
    data(){
        return {
        }
    }""" + pagehooks + """
}
</script>
<style lang="css" scoped>
"""+ cssimport +"""
</style>"""
    with open("../output/"+name+"/src/views/"+page.getPagename()+"View.vue","w") as f:
        f.write(vuepage)
    generatePageStyle(name,page)


def processTemplate(html_string,page):
    global components

    myhtml = html.fromstring(html_string)
    etree.indent(myhtml, space="    ")
    finalHtml = etree.tostring(myhtml, encoding='unicode', pretty_print=True)
    for p in components:
        for c in components[p]:
            pattern = "<"+c+">"+r"(\n[\s]*.*)*\n[\s]*"+r"<\/"+c+">"
            processedTemplate = re.sub(pattern,"<"+c.capitalize()+">"+"</"+c.capitalize()+">",finalHtml)
            finalHtml = processedTemplate
    return finalHtml

