from engine.stylegenerator import generatePageStyle, generateElemCssProperties, generateShapeCSS, generateShapeShadowCSS, generateVueSelectCssProperties, generateInputSearchFilterCssProperties, generateDatePickerCssProperties, generateSliderCssProperties,setComponentPositionCSS, generateRatingCssProperties, generatePaginatorCssProperties, generateFormCssProperties, generateCheckboxCssProperties, generateVideoCssProperties
from setup.vueprojectsetup import useSelectVuetifyPlugin, useIconFieldPrimevuePlugin, useDatePickerPrimevuePlugin, useSliderPrimevuePlugin, useRatingVuetifyPlugin, usePaginatorVuetifyPlugin, useFormPrimeVuePlugin, useCheckboxPrimeVuePlugin
from engine.logicgenerator import handleBehaviour,getpopulateDropdownFunction
from engine.assetshelper import getPrimeVueForm, getPrimeVueCheckbox
from parser.model.Mcomponent import Mcomponent
from parser.model.Melement import Melement
from parser.model.TextElement import TextElement
from parser.model.VideoElement import VideoElement
from parser.model.VectorElement import VectorElement
from parser.model.Dropdown import Dropdown
from parser.model.ShapeElement import ShapeElement
from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement

from bs4 import BeautifulSoup
import re
import itertools

allhooks = dict()
imports = dict()
components = dict()
auxiliarImports = dict()
componentAssets = dict()
allPagesInfo = dict()
allrefs = {}

def buildpage(name,page,pagesInfo,refs):
    global allhooks,imports,components,allPagesInfo,allrefs
    #setup a page
    allhooks[page.pagename] = {}
    imports[page.pagename] = []
    components[page.pagename] = set()
    auxiliarImports[page.pagename] = set()
    componentAssets[page.pagename] = []
    allrefs = refs
    allPagesInfo = pagesInfo
    output = ""  

    if(anyShapes(page.elements)==True): handleClipPathOverlaping(page.elements)
    for element in page.elements:
        output += processChildren(element,name,page)
    writeVue(name,page,output)

def processChildren(data,projectname,page):
    if(data==None): return ""
    if(len(data.children)>0):
        content=""
        output, endtag = applytransformation(data,projectname,page)
        for element in data.children:
            content += processChildren(element,projectname,page)

        return output + content + endtag

    else:
        output, endtag = applytransformation(data,projectname,page)
        output += endtag    
        return output

# Do a better handling of the tags
def applytransformation(elem,projectname,page):
    global allPagesInfo, allhooks, components, componentAssets, allrefs
    pagename = page.pagename
    cssclass = ""
    if(not isinstance(elem,Mcomponent)): cssclass = getElemId(elem.idElement)
    else: cssclass = getElemId(elem.idComponent)
    ref=""
    if(pagename in allrefs and cssclass in allrefs[pagename]):
        ref = f' ref="ref{cssclass}" '
    # insert directives and functions if there is some behaviour
    directives, hooks = handleBehaviour(elem,allPagesInfo,True)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[pagename].setdefault(hook, []).extend(hooks[hook])
    id = ""
    if(elem.style.getgridArea()!=None):
        id = ' id="'+elem.style.getgridArea()+'"'
    if(isinstance(elem,Mcomponent)):
        if(elem.getNameComponent()=="Dropdown" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useSelectVuetifyPlugin(projectname)
            options = ':items="allOptionValues'+str(cssclass)+'"'

            cssclass= "svueselect" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            placeholder = 'label="'+str(elem.placeholder)+'"'

            generateVueSelectCssProperties(projectname,pagename,cssclass,elem)
            return (f"<v-select {id}{ref}class="+'"grid-item '+ cssclass  + '" '+vmodel+' '+options+' '+placeholder, "/>")
        if(elem.getNameComponent()=="InputSearch" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useIconFieldPrimevuePlugin(projectname)
            cssclass= "ssearchinputfilter" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            placeholder = 'placeholder="'+str(elem.placeholder)+'"'
            generateInputSearchFilterCssProperties(projectname,pagename,cssclass,elem)
            componentAssets[pagename].extend([" IconField"," InputIcon"," InputText"])
            return (f'<IconField {id}{ref}class="{cssclass}"><InputIcon class="pi pi-search"/><InputText {vmodel} {placeholder} />','</IconField>')
        if(elem.getNameComponent()=="DatePicker" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useDatePickerPrimevuePlugin(projectname)
            cssclass= "sdatepicker" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            generateDatePickerCssProperties(projectname,pagename,cssclass,elem)
            componentAssets[pagename].extend([" DatePicker"])
            showicon = ""
            if(elem.style.getdropdownbackgroundcolor()!=None):
                showicon = ":showOnFocus='false' showIcon='' fluid=''"
            return (f'<DatePicker {id}{ref}{vmodel} class="{cssclass}" {showicon} >','</DatePicker>')
        if((elem.getNameComponent()=="ReadOnlyRating" or elem.getNameComponent()=="InteractiveRating") and elem.getTypeComponent()=="COMPONENT_ASSET"):
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
            return (f'<v-rating {id}{ref}class="{cssclass}" '+ f':length="{size}" :size="25" :model-value="{vmodel}" '+f" half-increments='' hover='' {readonlyconf} >",'</v-rating>')

        if(elem.getNameComponent()=="Slider" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useSliderPrimevuePlugin(projectname)
            cssclass= "sslider" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            generateSliderCssProperties(projectname,pagename,cssclass,elem)
            componentAssets[pagename].extend([" Slider"])
            return (f'<Slider {id}{ref}{vmodel} class="{cssclass}" >','</Slider>')
        if(elem.getNameComponent()=="Paginator" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            usePaginatorVuetifyPlugin(projectname)
            cssclass= "spaginator" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            generatePaginatorCssProperties(projectname,pagename,cssclass,elem)
            componentAssets[pagename].extend([" v-pagination"])
            return (f'<v-pagination {id}{ref}{vmodel} :total-visible="{elem.totalvisible}" :length="{elem.length}" class="{cssclass}" >','</v-pagination>')
        if(elem.getNameComponent()=="Form" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useFormPrimeVuePlugin(projectname)
            form = getPrimeVueForm(elem,cssclass,elem.inputs,elem.buttontxt)
            generateFormCssProperties(projectname,pagename,cssclass,elem,f"form{cssclass}",f"inputform{cssclass}",f"submitbtnform{cssclass}")
            auxiliarImports[pagename].add("import { ref } from 'vue'")
            componentAssets[pagename].extend([" Form"," InputText"," Message"])
            return form
        if(elem.getNameComponent()=="Checkbox" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useCheckboxPrimeVuePlugin(projectname)
            checkbox = getPrimeVueCheckbox(elem,cssclass)
            cssclass= "scheckbox" + cssclass
            generateCheckboxCssProperties(projectname,pagename,cssclass,f"label{cssclass}",elem)
            componentAssets[pagename].extend([" Checkbox"])
            return checkbox

    if(isinstance(elem, TextElement)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "p"
        txt = re.sub(r"\n", "<br/>",elem.text)
        return ("<"+ elem.tag + id + ref +" class="+'"grid-item text'+ cssclass  + '" '+ ' '.join(d for d in directives) +">"+txt, "</"+elem.tag+">")
    if(isinstance(elem, ContainerElement)):

        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "div"
        return ("<"+elem.tag + id + ref +" class="+'"grid-item container'+ cssclass + '" '+ ' '.join(d for d in directives) +">", "</"+elem.tag+">")
    if(isinstance(elem, ImageElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "img"
        return ("<"+elem.tag+ id + ref +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getimgpath() + '"' + ' '.join(d for d in directives) , "/>")
    if(isinstance(elem, VectorElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        return ("<"+elem.tag+ id + ref +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getsvgpath() + '"' + ' '.join(d for d in directives) , "/>")
    if(isinstance(elem, VideoElement)):
        cssclass= "svideo" + cssclass
        generateVideoCssProperties(projectname,pagename,cssclass,elem)
        return (f'<div {id}{ref}class="{cssclass}"><iframe width="{elem.style.getwidth()}px" height="{elem.style.getheight()}px" controls=1 src="{elem.getSrc()}">',"</iframe></div>")
    if(isinstance(elem, ShapeElement)):
        cssclassifier = ""
        cssclassifier = elem.getType().lower() + str(cssclass)

        generateShapeCSS(projectname,pagename,cssclassifier,elem.getType(),elem)

        begintag = "<div"+ id + ref +" class="+'"grid-item '+ cssclassifier + '" '+ ' '.join(d for d in directives) +">"
        endtag = "</div>"
        if(elem.style.boxShadow!=None): 
            wrapperclass = "wrapper" + cssclassifier
            begintag = "<div class="+'"grid-item '+ wrapperclass + '" ' +">"+begintag
            endtag = "</div>" + endtag
            generateShapeShadowCSS(projectname,pagename,wrapperclass,elem)

        return (begintag,endtag)
    if isinstance(elem, Mcomponent):
        componentName = elem.componentName.capitalize()
        classname = ' class="'+"grid-item-"+getElemId(elem.idComponent)+' component'+ getElemId(elem.idComponent)     
        if(elem.style.getPosition()!=None):
            classname += " pos"+componentName.lower()
            setComponentPositionCSS(projectname,pagename,"pos"+componentName.lower(),elem)
        components.setdefault(pagename, {}).add(elem.componentName.lower())
        return ("<"+componentName+f"{id}{ref}{classname}"+'" '+ ' '.join(d for d in directives) + ">","</"+componentName+">")
    return ("","")

def writeVue(name,page,content):
    global allhooks, components
    componentsimports=""
    for comp in components[page.getPagename()]:
        componentsimports += "import "+str(comp).capitalize()+" from '@/components/"+str(comp).capitalize()+".vue';\n" 
    for auximports in auxiliarImports[page.getPagename()]:
        componentsimports += auximports+";\n"
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    template = '<div class="grid-container">'+ content + '</div>'
    pagehooks=""
    allcomponents = (x.capitalize() for x in components[page.getPagename()])
    allcomponents = list(allcomponents)
    pagecomponents="""\n    components:{\n        """+ ',\n        '.join(allcomponents) +"""\n    },"""
    for hook in allhooks[page.getPagename()]:
        if("methods" in hook): pagehooks += hook + ":{\n"
        if("mounted" in hook): pagehooks += hook + "(){\n"
        if("setup" in hook): pagehooks += hook + "(){\n"
        for content in allhooks[page.getPagename()][hook]:
            if("methods" in hook): 
                pagehooks += content[1] + ",\n"
            if("mounted" in hook): 
                pagehooks += content[1] + "\n\n"
            if("setup" in hook): 
                pagehooks += content[1] + "\n\n"
        if(hook=="setup"): #writing the return statements from setup content
            pagehooks+="        return {\n          """
            for content in allhooks[page.getPagename()][hook]:
                for retstatement in content[0]:
                    pagehooks += "  "+retstatement + ",\n          "
            pagehooks += "}\n\n"
        pagehooks=pagehooks[:-2]+"\n\t},"
    pagehooks = pagehooks[:-1]
    if(len(pagehooks)>0): pagehooks= ",\n    "+pagehooks
    vuepage = """<template>\n""" + processTemplate(template,page.getPagename()) + """
</template>

<script>
"""+ componentsimports +"""
export default {"""+ pagecomponents +"""
    data(){
        return {
            """ + ',\n            '.join(str(key)+":"+str(value) for variables in page.getData() for key, value in variables.items()) + """    
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

    soup = BeautifulSoup(html_string, "html.parser")
    finalHtml = soup.prettify()
    for c in components[page]:
        pattern = "<"+c.lower()+r"([\s]*.*?)"+">"+r"(\n|.)*?"+r"<\/"+c.lower()+">"
        processedTemplate = re.sub(pattern,"<"+c.capitalize()+ r'\1' +">"+"</"+c.capitalize()+">",finalHtml)
        finalHtml = processedTemplate
    for c in componentAssets[page]:
        tag = c.split(" ")[1]
        pattern = "<"+tag.lower()+r"([\s]*.*?)"+">"+r"((\n|.)*?)"+r"<\/"+tag.lower()+">"
        processedTemplate = re.sub(pattern,"<"+tag+ r'\1' +">"+r'\2'+"</"+tag+">",finalHtml)
        if(tag=="DatePicker"):
            processedTemplate = re.sub('<DatePicker'+r"([\s]*.*?)"+'fluid="" showicon=""'+r'([\s]*.*?)'+'>',"<DatePicker"+r"\1 showIcon fluid \2>",processedTemplate)
        if(tag=="v-rating"):
            if(c.split(" ")[2]=="readonly"):
                processedTemplate = re.sub('<v-rating'+r"([\s]*.*?)"+'half-increments="" hover="" readonly=""'+r'([\s]*.*?)'+'>',"<v-rating"+r"\1 half-increments hover readonly \2>",processedTemplate)
        if(tag=="InputText"):
            processedTemplate = re.sub('<InputText'+r"([\s]*.*?)"+'fluid=""'+r'([\s]*.*?)'+'>',"<InputText"+r"\1 fluid \2>",processedTemplate)
        if(tag=="Form"):
            processedTemplate = re.sub('<Form'+r"([\s]*.*?)"+':initialvalues'+r'([\s]*.*?)'+':validateonblur'+r'([\s]*.*?)'+'>',"<Form"+r"\1 :initialValues\2 :validateOnBlur\3>",processedTemplate)

        finalHtml = processedTemplate
    return finalHtml


def handleClipPathOverlaping(elementos):
    elementos.reverse()
    repeatedElements = []
    for i in range(0,len(elementos)):
        for j in range(0,len(elementos)):
            if(i!=j and i<len(elementos) and j<len(elementos)):
                elem1 = elementos[j]
                elem2 = elementos[i]
                if(getValue(elem1.style.gridcolumnStart)>=getValue(elem2.style.gridcolumnStart) and
                    getValue(elem1.style.gridcolumnEnd)<=getValue(elem2.style.gridcolumnEnd) and
                    getValue(elem1.style.gridrowStart)>=getValue(elem2.style.gridrowStart) and
                    getValue(elem1.style.gridrowEnd)<=getValue(elem2.style.gridrowEnd) and
                    (isinstance(elem2,ShapeElement))):
                    elem2.children.append(elem1)
                    elem2.style.setDisplay("grid")
                    repeatedElements.append(j)

    for r in reversed(repeatedElements):
        if(r<len(elementos)): del elementos[r]

    for c in elementos:
        if(len(c.children)>0):
            handleClipPathOverlaping(c.children)
    elementos.reverse()

def getValue(value):
    if " span " in str(value):
        realvalue = value.split(" span ")[1] 
        return int(realvalue)
    else:
        return int(value) 

def anyShapes(elementos):
    allShapes = list(filter(lambda x: (isinstance(x,ShapeElement)),list(itertools.chain(*([x] + x.children for x in elementos)))))
    return len(allShapes) > 0

def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid
