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
    pattern = "[:;]"
    idcomponent = re.sub(pattern,"",component.idComponent)
    for element in component.children:
        output += processChildren(element,projectname,name,idcomponent)

    writeVueComponent(name,projectname,output,component,pagesInfo)


def processChildren(data,projectname,name,idcomponent):
    if(data==None): return ""
    if(len(data.children)>0):
        content=""
        output, endtag = applytransformation(data,projectname,name,idcomponent)
        for element in data.children:
            content += processChildren(element,projectname,name,idcomponent)

        return output + content + endtag

    else:
        output, endtag = applytransformation(data,projectname,name,idcomponent)
        output += endtag    
        return output

def applytransformation(elem,projectname,pagename,idcomponent):
    global allhooks
    cssclass = ""
    pattern = "[:;]"
    if(not isinstance(elem,Mcomponent)): cssclass = re.sub(pattern,"",elem.idElement)
    else: cssclass = re.sub(pattern,"",elem.idComponent)
    if(isinstance(elem, TextElement)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        #iterate the list of interactions (logicgenerator.py)
        if(elem.tag==""):
            elem.tag = "p"
        return ("<"+elem.tag+" class="+'"grid-item-'+ idcomponent +' text'+ cssclass +'">'+elem.text, "</"+elem.tag+">")
    if(isinstance(elem, ContainerElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "p"
        #iterate the list of interactions (logicgenerator.py)
        directives = []
        html = "<"+elem.tag+" class="+'"grid-item-'+ idcomponent +' container'+ cssclass + '" '+ ' '.join(d for d in directives) +">"
        return (html, "</"+elem.tag+">")
    return ("","")

def writeVueComponent(name,project_name,content,component,pagesInfo):
    global allhooks 
    pattern = "[:;]"
    idcomponent = re.sub(pattern,"",component.idComponent)
    cssimport = "@import '../assets/"+name+".css';"
    pagehooks=""

    directives, hooks = handleBehaviour(component,pagesInfo,component.getData())
    if(hooks!=None): 
        for hook in hooks:
            allhooks[name].setdefault(hook, []).extend(hooks[hook])

    for hook in allhooks[name]:
        pagehooks = hook + ":{\n"
        for chook in allhooks[name][hook]:
            pagehooks += chook[1] + ",\n"
        pagehooks = pagehooks[:-2]
        pagehooks +="\n\t}"
    if(len(pagehooks)>0): pagehooks = ",\n    "+pagehooks
    template = '<div class="grid-item-'+idcomponent+' component'+ idcomponent +'"'+ ' '.join(d for d in directives) + ">"+ content + '</div>'
    componentpage = """<template>\n""" + processTemplate(template) + """
</template>

<script>
export default {
    data(){
        return {
        }
    }""" + pagehooks + """
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

