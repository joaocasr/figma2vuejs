from engine.stylegenerator import generatePageStyle, generateComponentStyle, generateElemCssProperties, generateShapeCSS, generateRatingCssProperties
from setup.vueprojectsetup import useRatingVuetifyPlugin
from engine.logicgenerator import handleBehaviour
from parser.model.Mcomponent import Mcomponent
from parser.model.Melement import Melement
from parser.model.TextElement import TextElement
from parser.model.VectorElement import VectorElement
from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement
from parser.model.ShapeElement import ShapeElement
from parser.model.Rating import Rating
from parser.model.RatingStyle import RatingStyle

from bs4 import BeautifulSoup
import itertools
import re

allhooks = dict()
allpagesInfo = {}
componentAssets = dict()

def buildcomponent(component,projectname,pagesInfo):
    global allhooks,allpagesInfo
    name = component.componentName
    allhooks[name] = {}
    componentAssets[name] = []
    # build elements from the component  
    allpagesInfo = pagesInfo
    output = ""
    idcomponent = getElemId(component.idComponent)

    (flattenElements,allShapes) = flattenAndShapes(component)
    onstack = filterOverlapingElements(allShapes,flattenElements)
    handleClipPathOverlaping(component,onstack)

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
    global allhooks, allpagesInfo
    cssclass = ""
    if(not isinstance(elem,Mcomponent)): cssclass = getElemId(elem.idElement)
    else: cssclass = getElemId(elem.idComponent)
    
    directives, hooks = handleBehaviour(elem,allpagesInfo,False)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[pagename].setdefault(hook, []).extend(hooks[hook])

    if(isinstance(elem, TextElement)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        #iterate the list of interactions (logicgenerator.py)
        if(elem.tag==""):
            elem.tag = "p"
        return ("<"+elem.tag+" class="+'"grid-item-'+ idcomponent +' text'+ cssclass +'" '+' '.join(d for d in directives)+'>'+elem.text, "</"+elem.tag+">")
    if(isinstance(elem, ContainerElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "div"
        #iterate the list of interactions (logicgenerator.py)
        #directives = []
        html = "<"+elem.tag+" class="+'"grid-item-'+ idcomponent +' container'+ cssclass + '" '+ ' '.join(d for d in directives) +">"
        return (html, "</"+elem.tag+">")
    if(isinstance(elem, ShapeElement)):
        cssclassifier = ""
        cssclassifier = elem.getType().lower() + str(cssclass)
        generateShapeCSS(projectname,pagename,cssclassifier,elem.getType(),elem)
    
        #directives = []
        html = "<div class="+'"grid-item-'+ idcomponent +' '+ cssclassifier + '" '+ ' '.join(d for d in directives) +">"
        return (html, "</div>")
    if(isinstance(elem, ImageElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "img"
        return ("<"+elem.tag +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getimgpath() + '"' + ' '.join(d for d in directives) , "/>")
    
    if(isinstance(elem, VectorElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        return ("<"+elem.tag +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getsvgpath() + '"' + ' '.join(d for d in directives) , "/>")

        return (begintag,endtag)

    if(isinstance(elem, Mcomponent) and (elem.getNameComponent()=="ReadOnlyRating" or elem.getNameComponent()=="InteractiveRating")):
        useRatingVuetifyPlugin(projectname)
        cssclass= "srating" + cssclass
        vmodel = str(elem.vmodel)
        size = str(elem.nrstars)
        readonly = elem.readonly
        generateRatingCssProperties(projectname,pagename,cssclass,elem)
        readonlyconf =""
        if(readonly==True):
            readonlyconf = "readonly=''"
            componentAssets[pagename].extend([" v-rating readonly"])
        return (f'<v-rating class="{cssclass}" '+ f':length="{size}" :size="25" :model-value="{vmodel}" '+f" half-increments='' hover='' {readonlyconf} >",'</v-rating>')

    return ("","")

def writeVueComponent(name,project_name,content,component,pagesInfo):
    global allhooks 
    pattern = "[:;]"
    idcomponent = getElemId(component.idComponent)
    cssimport = "@import '../assets/"+name.lower()+".css';"
    pagehooks=""
    for hook in allhooks[name]:
        pagehooks = hook + ":{\n"
        for chook in allhooks[name][hook]:
            pagehooks += chook[1] + ",\n"
        pagehooks = pagehooks[:-2]
        pagehooks +="\n\t}"
    if(len(pagehooks)>0): pagehooks = ",\n    "+pagehooks
    template = '<div>' + content + '</div>' #'<div class="grid-item-'+idcomponent+' component'+ idcomponent +'"'+ ">"+ content + '</div>'
    componentpage = """<template>\n""" + processTemplate(template,name) + """
</template>

<script>
export default {
    data(){
        return {
        """ + ',\n            '.join(str(key)+":"+str(value) for variables in component.getData() for key, value in variables.items()) + """   
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


def processTemplate(html_string,name):
    soup = BeautifulSoup(html_string, "html.parser")
    finalHtml = soup.prettify()
    for c in componentAssets[name]:
        tag = c.split(" ")[1]
        pattern = "<"+tag.lower()+r"([\s]*.*?)"+">"+r"((\n|.)*?)"+r"<\/"+tag.lower()+">"
        processedTemplate = re.sub(pattern,"<"+tag+ r'\1' +">"+r'\2'+"</"+tag+">",finalHtml)
        if(tag=="DatePicker"):
            processedTemplate = re.sub('<DatePicker'+r"([\s]*.*?)"+'fluid="" showicon=""'+r'([\s]*.*?)'+'>',"<DatePicker"+r"\1 showIcon fluid \2>",processedTemplate)
        if(tag=="v-rating"):
            if(c.split(" ")[2]=="readonly"):
                processedTemplate = re.sub('<v-rating'+r"([\s]*.*?)"+'half-increments="" hover="" readonly=""'+r'([\s]*.*?)'+'>',"<v-rating"+r"\1 half-increments hover readonly \2>",processedTemplate)
        finalHtml = processedTemplate
    return finalHtml

def filterOverlapingElements(allShapes,allElements):
    allElements.reverse()
    onstack = []
    for e in allElements:
        if(not isinstance(e,ShapeElement)):
            for s in allShapes:
                elem1 = e
                elem2 = s
                if(elem1.style.gridcolumnStart>=elem2.style.gridcolumnStart and
                    elem1.style.gridcolumnEnd<=elem2.style.gridcolumnEnd and
                    elem1.style.gridrowStart>=elem2.style.gridrowStart and
                    elem1.style.gridrowEnd<=elem2.style.gridrowEnd and
                    (isinstance(elem2,ShapeElement))):
                        onstack.append((elem1,elem2))
    return onstack

def handleClipPathOverlaping(component,onstack):
    component.children.reverse()
    toremove = set()
    for i in component.children:
        for s in onstack:
            if(isinstance(i,Melement) and isinstance(s[0],Melement) and i.idElement==s[0].idElement):
                toremove.add(i) 
            if(isinstance(i,Melement) and isinstance(s[1],ShapeElement) and i.idElement==s[1].idElement):
                i.style.setDisplay("grid")
                i.children.append(s[0])
        for c in i.children:
            handleClipPathOverlaping(c,onstack)
    component.children = [child for child in component.children if child not in toremove]
    component.children.reverse()

def flattenAndShapes(component):
    flattenElements = list(itertools.chain(*([x] + x.children for x in component.children)))
    allShapes = list(filter(lambda x: (isinstance(x,ShapeElement)),flattenElements))
    return (flattenElements,allShapes)


def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid
