from engine.stylegenerator import generatePageStyle, generateComponentStyle, generateElemCssProperties
from engine.logicgenerator import handleBehaviour
from parser.model.Mcomponent import Mcomponent
from parser.model.TextElement import TextElement
from parser.model.ContainerElement import ContainerElement

import xml.etree.ElementTree as ET
from lxml import etree, html
import re

allhooks = dict()

def buildcomponent(component,projectname,pagesInfo):
    global allhooks
    name = component.componentName
    allhooks[name] = {}
    # build elements from the component  
    output = ""
    for element in component.children:
        output += processChildren(element,projectname,name)

    writeVueComponent(name,projectname,output,component,pagesInfo)


def processChildren(data,projectname,name):
    if(data==None): return ""
    if(len(data.children)>0):
        content=""
        output, endtag = applytransformation(data,projectname,name)
        for element in data.children:
            content += processChildren(element,projectname,name)

        return output + content + endtag

    else:
        output, endtag = applytransformation(data,projectname,name)
        output += endtag    
        return output

def applytransformation(elem,projectname,pagename):
    global allhooks
    cssclass = ""
    pattern = "[:;]"
    if(not isinstance(elem,Mcomponent)): cssclass = re.sub(pattern,"",elem.idElement)
    else: cssclass = re.sub(pattern,"",elem.idComponent)
    if isinstance(elem, TextElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
            #iterate the list of interactions (logicgenerator.py)
            return ("<p class="+'"grid-item text'+ cssclass +'">'+elem.text, "</p>")
    if isinstance(elem, ContainerElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
            #iterate the list of interactions (logicgenerator.py)
            directives = []
            html = "<div class="+'"grid-item container'+ cssclass + '" '+ ' '.join(d for d in directives) +">"
            return (html, "</div>")

def writeVueComponent(name,project_name,content,component,pagesInfo):
    global allhooks 
    pattern = "[:;]"
    idcomponent = re.sub(pattern,"",component.idComponent)
    cssimport = "@import '../assets/"+name+".css';"
    pagehooks=""

    directives, hooks = handleBehaviour(component,pagesInfo)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[name].setdefault(hook, []).extend(hooks[hook])

    for hook in allhooks[name]:
        pagehooks = hook + ":{\n"
        for chook in allhooks[name][hook]:
            pagehooks += chook + ",\n"
        pagehooks = pagehooks[:-2]
        pagehooks +="\n\t}"

    template = '<div class="component'+ idcomponent +'"'+ ' '.join(d for d in directives) + ">"+ content + '</div>'
    componentpage = """<template>\n""" + processTemplate(template) + """
</template>

<script>
export default {
    data(){
        return {
        }
    },
    """ + pagehooks + """
}
</script>
<style lang="css" scoped>
"""+ cssimport +"""
</style>"""
    with open("../output/"+project_name+"/src/components/"+name.capitalize()+".vue","w") as f:
        f.write(componentpage)
    generateComponentStyle(project_name,component)


def processTemplate(html_string):
    myhtml = html.fromstring(html_string)
    etree.indent(myhtml, space="    ")
    finalHtml = etree.tostring(myhtml, encoding='unicode', pretty_print=True)
    
    return finalHtml

