from engine.stylegenerator import generatePageStyle, generateElemCssProperties, generateShapeCSS, generateShapeShadowCSS, generateVueSelectCssProperties, generateInputSearchFilterCssProperties, generateDatePickerCssProperties, generateSliderCssProperties
from setup.vueprojectsetup import installVue3select_dependency, useIconFieldPrimevuePlugin, useDatePickerPrimevuePlugin, useSliderPrimevuePlugin
from engine.logicgenerator import handleBehaviour
from parser.model.Mcomponent import Mcomponent
from parser.model.TextElement import TextElement
from parser.model.Dropdown import Dropdown
from parser.model.ShapeElement import ShapeElement
from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement

from bs4 import BeautifulSoup
import re

allhooks = dict()
imports = dict()
components = dict()
componentAssets = dict()
primeVueComponents = dict()
allPagesInfo = dict()

def buildpage(name,page,pagesInfo):
    global allhooks,imports,components,allPagesInfo
    #setup a page
    allhooks[page.pagename] = {}
    imports[page.pagename] = []
    components[page.pagename] = []
    componentAssets[page.pagename] = []
    primeVueComponents[page.pagename] = []
    allPagesInfo = pagesInfo
    output = ""  
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
    global allPagesInfo, allhooks, components, componentAssets
    pagename = page.pagename
    cssclass = ""
    pattern = "[:;]"
    if(not isinstance(elem,Mcomponent)): cssclass = re.sub(pattern,"",elem.idElement)
    else: cssclass = re.sub(pattern,"",elem.idComponent)
    
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
            installVue3select_dependency(projectname)
            componentAssets[pagename].append('import VueSelect from "vue3-select-component";')
            options = ':options="allOptions'+str(cssclass)+'"'
            cssclass= "svueselect" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            ismulti = ':is-multi="'+str(elem.ismulti)+'"'
            placeholder = 'placeholder="'+str(elem.placeholder)+'"'

            generateVueSelectCssProperties(projectname,pagename,cssclass,elem)
            return ("<VueSelect class="+'"grid-item '+ cssclass  + '" '+vmodel+' '+ismulti+' '+options+' '+placeholder, "/>")
        if(elem.getNameComponent()=="InputSearch" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useIconFieldPrimevuePlugin(projectname)
            cssclass= "ssearchinputfilter" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            placeholder = 'placeholder="'+str(elem.placeholder)+'"'
            generateInputSearchFilterCssProperties(projectname,pagename,cssclass,elem)
            primeVueComponents[pagename].extend([" IconField"," InputIcon"," InputText"])
            return (f'<IconField class="{cssclass}"><InputIcon class="pi pi-search"/><InputText {vmodel} {placeholder} />','</IconField>')
        if(elem.getNameComponent()=="DatePicker" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useDatePickerPrimevuePlugin(projectname)
            cssclass= "sdatepicker" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            generateDatePickerCssProperties(projectname,pagename,cssclass,elem)
            primeVueComponents[pagename].extend([" DatePicker"])
            showicon = ""
            if(elem.style.getdropdownbackgroundcolor()!=None):
                showicon = ":showOnFocus='false' showIcon='' fluid=''"
            return (f'<DatePicker {vmodel} class="{cssclass}" {showicon} >','</DatePicker>')
        if(elem.getNameComponent()=="Slider" and elem.getTypeComponent()=="COMPONENT_ASSET"):
            useSliderPrimevuePlugin(projectname)
            cssclass= "sslider" + cssclass
            vmodel = 'v-model="'+str(elem.vmodel)+'"'
            generateSliderCssProperties(projectname,pagename,cssclass,elem)
            primeVueComponents[pagename].extend([" Slider"])
            return (f'<Slider {vmodel} class="{cssclass}" >','</Slider>')

    if(isinstance(elem, TextElement)):
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "p"
        txt = re.sub(r"\n", "<br/>",elem.text)
        return ("<"+ elem.tag +" class="+'"grid-item text'+ cssclass  + '" '+ ' '.join(d for d in directives) +">"+txt, "</"+elem.tag+">")
    if(isinstance(elem, ContainerElement)):

        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "div"
        return ("<"+elem.tag + id +" class="+'"grid-item container'+ cssclass + '" '+ ' '.join(d for d in directives) +">", "</"+elem.tag+">")
    if(isinstance(elem, ImageElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        if(elem.tag==""):
            elem.tag = "img"
        return ("<"+elem.tag+ id +" class="+'"grid-item container'+ cssclass + '" '+ 'src="' + elem.getimgpath() + '"' + ' '.join(d for d in directives) , "/>")
    if(isinstance(elem, ShapeElement)):
        cssclassifier = ""
        cssclassifier = elem.getType().lower() + str(cssclass)

        generateShapeCSS(projectname,pagename,cssclassifier,elem.getType(),elem)

        begintag = "<div"+ id +" class="+'"grid-item '+ cssclassifier + '" '+ ' '.join(d for d in directives) +">"
        endtag = "</div>"
        if(elem.style.boxShadow!=None): 
            wrapperclass = "wrapper" + cssclassifier
            begintag = "<div class="+'"grid-item '+ wrapperclass + '" ' +">"+begintag
            endtag = "</div>" + endtag
            generateShapeShadowCSS(projectname,pagename,wrapperclass,elem)

        return (begintag,endtag)
    if isinstance(elem, Mcomponent):
        componentName = elem.componentName.capitalize()
        components.setdefault(pagename, []).append(elem.componentName.lower())
        return ("<"+componentName+" "+ ' '.join(d for d in directives) + ">","</"+componentName+">")
    return ("","")

def writeVue(name,page,content):
    global allhooks, components, componentAssets
    componentsimports=""
    for comp in components[page.getPagename()]:
        componentsimports += "import "+str(comp).capitalize()+" from '@/components/"+str(comp).capitalize()+".vue';\n" 
    for comp in componentAssets[page.getPagename()]:
        componentsimports += comp + "\n"
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    template = '<div class="grid-container">'+ content + '</div>'
    pagehooks=""
    allcomponents = (x.capitalize() for x in components[page.getPagename()])
    allcomponents = list(allcomponents)
    for x in componentAssets[page.getPagename()]:
        allcomponents.append(x.split(" ")[1])
    pagecomponents="""\n    components:{\n        """+ ',\n        '.join(allcomponents) +"""\n    },"""
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
        pattern = "<"+c.lower()+r"([\s]*.*?)"+">"+r"(\n|.)*"+r"<\/"+c.lower()+">"
        processedTemplate = re.sub(pattern,"<"+c.capitalize()+ r'\1' +">"+"</"+c.capitalize()+">",finalHtml)
        finalHtml = processedTemplate
    componentAssets[page].extend(primeVueComponents[page])
    for c in componentAssets[page]:
        tag = c.split(" ")[1]
        pattern = "<"+tag.lower()+r"([\s]*.*?)"+">"+r"((\n|.)*?)"+r"<\/"+tag.lower()+">"
        processedTemplate = re.sub(pattern,"<"+tag+ r'\1' +">"+r'\2'+"</"+tag+">",finalHtml)
        if(tag=="DatePicker"):
            processedTemplate = re.sub('<DatePicker'+r"([\s]*.*?)"+'fluid="" showicon=""'+r'([\s]*.*?)'+'>',"<DatePicker"+r"\1 showIcon fluid \2>",processedTemplate,)
        finalHtml = processedTemplate
    return finalHtml

