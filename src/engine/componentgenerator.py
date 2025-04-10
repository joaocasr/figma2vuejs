from engine.stylegenerator import generatePageStyle, generateComponentStyle, generateElemCssProperties, generateShapeCSS, generateRatingCssProperties, generateMenuCssProperties, setComponentPositionCSS, generateInputSearchFilterCssProperties
from setup.vueprojectsetup import useRatingVuetifyPlugin,useMenuVuetifyPlugin, useIconFieldPrimevuePlugin
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
from engine.assetshelper import getVuetifyMenu
from utils.processing import getFormatedName,getElemId,doesImageExist

from bs4 import BeautifulSoup
import itertools
import re

allhooks = dict()
allpagesInfo = {}
componentAssets = dict()
allrefs = {}
nestedComponents = {}

def buildcomponent(component,projectname,pagesInfo,refs):
    global allhooks,allpagesInfo,allrefs,nestedComponents
    name = component.componentName
    allhooks[name] = {}
    componentAssets[name] = []
    nestedComponents[name] = set()
    allrefs = refs
    # build elements from the component  
    allpagesInfo = pagesInfo
    output = ""
    idcomponent = getElemId(component.idComponent)

    
    if(anyShapes(component.children)==True): handleClipPathOverlaping(component.children)

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
    global allhooks, allpagesInfo, allrefs, nestedComponents
    cssclass = ""
    if(not isinstance(elem,Mcomponent)): cssclass = getElemId(elem.idElement)
    else: cssclass = getElemId(elem.idComponent)
    ref=""
    if(pagename in allrefs and cssclass in allrefs[pagename]):
        ref = f' ref="ref{cssclass}" '

    directives, hooks = handleBehaviour(elem,allpagesInfo,pagename,False)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[pagename].setdefault(hook, []).extend(hooks[hook])

    if(isinstance(elem, TextElement)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "p"
        return ("<"+elem.tag+f" {ref}class="+'"grid-item-'+ idcomponent +' text'+ cssclass +'" '+' '.join(d for d in directives)+'>'+elem.text, "</"+elem.tag+">")
    if(isinstance(elem, ContainerElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "div"
        html = "<"+elem.tag+f" {ref}class="+'"grid-item-'+ idcomponent +' container'+ cssclass + '" '+ ' '.join(d for d in directives) +">"
        return (html, "</"+elem.tag+">")
    if(isinstance(elem, ShapeElement)):
        cssclassifier = ""
        cssclassifier = elem.getType().lower() + str(cssclass)
        generateShapeCSS(projectname,pagename,cssclassifier,elem.getType(),elem)
    
        html = f"<div {ref}class="+'"grid-item-'+ idcomponent +' '+ cssclassifier + '" '+ ' '.join(d for d in directives) +">"
        return (html, "</div>")
    if(isinstance(elem, ImageElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "img"
        doesImageExist(elem.getimgpath(),elem,projectname)
        return ("<"+elem.tag +f" {ref}class="+'"grid-item-'+ idcomponent + ' container'+ cssclass + '" '+ 'src="' + elem.getimgpath() + '"' + ' '.join(d for d in directives) , "/>")
    
    if(isinstance(elem, VectorElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        doesImageExist(elem.getsvgpath(),elem,projectname)
        return ("<"+elem.tag +f" {ref}class="+'"grid-item-'+idcomponent+' container'+ cssclass + '" '+ 'src="' + elem.getsvgpath() + '"' + ' '.join(d for d in directives) , "/>")

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
        return (f'<v-rating class="grid-item-' + idcomponent + f' {cssclass}" ' + f':length="{size}" :size="25" :model-value="{vmodel}" '+f" half-increments='' hover='' {readonlyconf} >",'</v-rating>')

    if(isinstance(elem, Mcomponent) and (elem.getNameComponent()=="Menu")):
        useMenuVuetifyPlugin(projectname)
        menu = getVuetifyMenu(elem,cssclass,idcomponent)
        generateMenuCssProperties(projectname,pagename,"smenu"+cssclass,elem)
        componentAssets[pagename].extend([" v-menu"," v-list"])
        return menu

    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="InputSearch"):
        useIconFieldPrimevuePlugin(projectname)
        cssclass= "ssearchinputfilter" + cssclass
        vmodel = 'v-model="'+str(elem.vmodel)+'"'
        placeholder = 'placeholder="'+str(elem.placeholder)+'"'
        generateInputSearchFilterCssProperties(projectname,pagename,cssclass,elem)
        componentAssets[pagename].extend([" IconField"," InputIcon"," InputText"])
        return (f'<IconField class="{cssclass}"><InputIcon class="pi pi-search"/><InputText {vmodel} {placeholder} />','</IconField>')

    if(isinstance(elem, Mcomponent)):
        componentName = getFormatedName(elem.componentName.capitalize())
        classname = ' class="'+"grid-item-"+getElemId(elem.idComponent)+' component'+ getElemId(elem.idComponent)     
        if(elem.style.getPosition()!=None):
            classname += " pos"+componentName.lower()
            setComponentPositionCSS(projectname,pagename,"pos"+componentName.lower(),elem)
        nestedComponents.setdefault(pagename, {}).add(getFormatedName(elem.componentName.lower()))
        return ("<"+componentName+f"{ref}{classname}"+'" '+ ' '.join(d for d in directives) + ">","</"+componentName+">")

    return ("","")

def writeVueComponent(name,project_name,content,component,pagesInfo):
    global allhooks 
    componentsimports="\n"
    for comp in nestedComponents[name]:
        componentsimports += "import "+getFormatedName(str(comp).capitalize())+" from '@/components/"+getFormatedName(str(comp).capitalize())+".vue';\n" 
    cssimport = "@import '../assets/"+getFormatedName(name.lower())+".css';"
    pagehooks=""
    pagecomponents = ""
    allcomponents = (x.capitalize() for x in nestedComponents[name])
    allcomponents = list(allcomponents)
    if(len(allcomponents)>0): pagecomponents="""\n    components:{\n        """+ ',\n        '.join(allcomponents) +"""\n    },"""
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

<script>"""+ componentsimports +"""export default {"""+ pagecomponents +"""
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
    with open("../output/"+project_name+"/src/components/"+getFormatedName(name.capitalize())+".vue","w") as f:
        f.write(componentpage)
    generateComponentStyle(project_name,component)


def processTemplate(html_string,name):
    soup = BeautifulSoup(html_string, "html.parser")
    finalHtml = soup.prettify()
    for c in nestedComponents[name]:
        pattern = "<"+c.lower()+r" ([\s]*.*?)"+">"+r"((\n|.)*?)"+r"<\/"+c.lower()+">"
        processedTemplate = re.sub(pattern,"<"+c.capitalize()+ r' \1' +">"+"</"+c.capitalize()+">",finalHtml)
        finalHtml = processedTemplate
    for c in componentAssets[name]:
        tag = c.split(" ")[1]
        pattern = "<"+tag.lower()+r" ([\s]*.*?)"+">"+r"((\n|.)*?)"+r"<\/"+tag.lower()+">"
        processedTemplate = re.sub(pattern,"<"+tag+ r' \1' +">"+r'\2'+"</"+tag+">",finalHtml)
        if(tag=="DatePicker"):
            processedTemplate = re.sub('<DatePicker'+r" ([\s]*.*?)"+'fluid="" showicon=""'+r'([\s]*.*?)'+'>',"<DatePicker"+r" \1 showIcon fluid \2>",processedTemplate)
        if(tag=="v-rating"):
            if(c.split(" ")[2]=="readonly"):
                processedTemplate = re.sub('<v-rating'+r" ([\s]*.*?)"+'half-increments="" hover="" readonly=""'+r'([\s]*.*?)'+'>',"<v-rating"+r" \1 half-increments hover readonly \2>",processedTemplate)
        finalHtml = processedTemplate
    return finalHtml

def filterOverlapingElements(component,onstack):
    elements = component.children
    alllevelShapes = getShapes(elements)
    idel=-1
    idsh=-1
    if(len(alllevelShapes)>0):
        for s in alllevelShapes:
            idsh+=1
            for i in component.children:
                idel+=1
                if(i!=s and idsh<idel and getValue(i.style.gridcolumnStart)>=getValue(s.style.gridcolumnStart) and
                    getValue(i.style.gridcolumnEnd)<=getValue(s.style.gridcolumnEnd) and
                    getValue(i.style.gridrowStart)>=getValue(s.style.gridrowStart) and
                    getValue(i.style.gridrowEnd)<=getValue(s.style.gridrowEnd) and
                    (isinstance(s,ShapeElement))):
                        onstack.append((i,s))
                for c in i.children:
                    if(len(c.children)>0): filterOverlapingElements(c,onstack)
    return onstack

def getShapes(elementos):
    return list(filter(lambda x: (isinstance(x,ShapeElement)),elementos))

def handleClipPathOverlaping(elementos):
    repeatedElements = []
    for i, elem2 in enumerate(elementos):
        for j, elem1 in enumerate(elementos):
            if i != j:
                if (getValue(elem1.style.gridcolumnStart) >= getValue(elem2.style.gridcolumnStart) and
                    getValue(elem1.style.gridcolumnEnd) <= getValue(elem2.style.gridcolumnEnd) and
                    getValue(elem1.style.gridrowStart) >= getValue(elem2.style.gridrowStart) and
                    getValue(elem1.style.gridrowEnd) <= getValue(elem2.style.gridrowEnd) and
                    isinstance(elem2, ShapeElement)):
                    elem2.children.append(elem1)
                    elem2.style.setDisplay("grid")
                    repeatedElements.append(j)

    for index in sorted(set(repeatedElements), reverse=True):
        del elementos[index]

    for c in elementos:
        if(len(c.children)>0):
            handleClipPathOverlaping(c.children)
    
def flatTree(elementos):
    for node in elementos:
        yield node
        if node.children:
            yield from flatTree(node.children)

def anyShapes(elementos):
    allShapes = list(filter(lambda x: (isinstance(x,ShapeElement)),list(flatTree(elementos))))
    return len(allShapes) > 0

def getValue(value):
    if(value==None): return 0
    if(isinstance(value, int)): return value
    if(value.isnumeric()): return int(value)
    if(" span " in str(value)):
        realvalue = value.split(" span ")[1] 
        return int(realvalue)