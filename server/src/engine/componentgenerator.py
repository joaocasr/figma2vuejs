from engine.stylegenerator import generateComponentStyle, generateElemCssProperties, generateShapeCSS, generateRatingCssProperties, generateMenuCssProperties, setComponentPositionCSS, generateInputSearchFilterCssProperties, generateDatePickerCssProperties, generateFormCssProperties, generateTableCssProperties, generateSliderCssProperties, generatePaginatorCssProperties, generateVueSelectCssProperties, generateCheckboxCssProperties, updateZIndex, generateTransitionAnimation
from setup.vueprojectsetup import useRatingVuetifyPlugin,useMenuVuetifyPlugin, useIconFieldPrimevuePlugin, useDatePickerPrimevuePlugin, useFormPrimeVuePlugin, useDataTablePrimevuePlugin, useSliderPrimevuePlugin, usePaginatorVuetifyPlugin, useSelectVuetifyPlugin, useCheckboxPrimeVuePlugin, useToastPrimeVuePlugin
from engine.logicgenerator import handleBehaviour,getTextDestination,getKeyEventsFunction,hasAnimationVar, addSetAnimationVarFunction
from parser.model.Mcomponent import Mcomponent
from engine.assetshelper import getPrimeVueForm, getPrimeVueCheckbox, getVuetifyMenu, getPrimeVueDataTable
from parser.model.TextElement import TextElement
from parser.model.VectorElement import VectorElement
from parser.model.ContainerElement import ContainerElement
from parser.model.ImageElement import ImageElement
from parser.model.ShapeElement import ShapeElement
from engine.assetshelper import getVuetifyMenu
from utils.tools import getFormatedName,getElemId,doesImageExist,getId

from bs4 import BeautifulSoup
import re

allhooks = dict()
allpagesInfo = {}
componentAssets = dict()
allrefs = {}
nestedComponents = {}
allvariants = []
componentMethods = {}
alltransitionodes = []
allEmissionpaths = {}
allclosePaths = {}
allProps = {}
auxiliarImports = dict()
pagename=""
globalprojectname=""
componentData = {}

def buildcomponent(component,projectname,pagesInfo,refs,variants,transition_nodeIds,event_EmissionPaths,closePaths):
    global pagename,globalprojectname,allhooks,allpagesInfo,allrefs,nestedComponents,allvariants,allProps,componentData,alltransitionodes,allEmissionpaths,allclosePaths
    name = component.getNameComponent()
    allhooks[name] = {}
    auxiliarImports[name] = set()
    componentAssets[name] = []
    nestedComponents[name] = set()
    allrefs = refs
    allProps = component.getProps()
    componentData = component.getData()
    allEmissionpaths = event_EmissionPaths
    allclosePaths = closePaths 
    # build elements from the component  
    allpagesInfo = pagesInfo
    output = ""
    idcomponent = getElemId(component.getIdComponent())
    pagename=name
    globalprojectname=projectname
    # the position of the variants will be the same as their default variant instance
    for v in variants:
        for c in v.variantComponents:
            if(component.getNameComponent()==c.getNameComponent()):
                updatePositions(component,v.variantComponents)

    allvariants = variants
    alltransitionodes = transition_nodeIds
    if(hasAnimationVar(component.getData())):
        componentAssets[name].extend([" Transition"])
        addSetAnimationVarFunction(allhooks,pagename)
    if(anyShapes(component.getChildren())==True): handleClipPathOverlaping(component.getChildren())
    if(len(component.interactions)>0 and len(component.getChildren())>0): component.getChildren()[0].interactions.extend(component.interactions)
    for element in component.getChildren():
        output += processChildren(element,projectname,name,idcomponent)

    writeVueComponent(name,projectname,output,component,pagesInfo)


def processChildren(data,projectname,name,idcomponent):
    if(data==None): return ""
    if(len(data.getChildren())>0):
        content=""
        output, endtag = applytransformation(data,projectname,name,idcomponent)
        output, endtag = insertTransitionComponent(data,output, endtag)
        for element in data.getChildren():
            content += processChildren(element,projectname,name,idcomponent)

        return output + content + endtag

    else:
        output, endtag = applytransformation(data,projectname,name,idcomponent)
        output, endtag = insertTransitionComponent(data,output, endtag)
        output += endtag    
        return output

def applytransformation(elem,projectname,pagename,idcomponent):
    global allhooks, allpagesInfo, allrefs, nestedComponents, allvariants, allProps, componentData, allEmissionpaths, allclosePaths
    cssclass = ""
    if(not isinstance(elem,Mcomponent)): cssclass = getElemId(elem.getIdElement())
    else: cssclass = getElemId(elem.getIdComponent())
    ref=""
    id=""
    if(pagename in allrefs and cssclass in allrefs[pagename]):
        ref = f' ref="ref{cssclass}" '
    if(elem.style.getgridArea()!=None):
        id = ' id="'+elem.style.getgridArea()+'"'
    directives, hooks = handleBehaviour(elem,allpagesInfo,pagename,False,allvariants,componentData,allEmissionpaths,allclosePaths)
    if(hooks!=None): 
        for hook in hooks:
            allhooks[pagename].setdefault(hook, []).extend(hooks[hook])
    generateActionsAnimationStyle(projectname,pagename,cssclass,elem)
    if(isinstance(elem, TextElement)):
        if(elem.tag==""):
            elem.tag = "p"
        txtContent = elem.text
        href = getTextDestination(elem,allpagesInfo)
        if(href!=None):
            elem.tag = "a"
            href = 'href="/'+href+'" '
        else: href = ""
        generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
        if("atr"+cssclass in allProps.keys()):
            txtContent = "{{"+ f"atributes.atr{cssclass}" +"}}"
        return ("<"+elem.tag+f" {href}{ref}class="+'"grid-item-'+ idcomponent +' text'+ cssclass +'" '+' '.join(d for d in directives)+'>'+txtContent, "</"+elem.tag+">")
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
        imgPath = 'src="'+elem.getimgpath()+'"'
        if("atr"+cssclass in allProps.keys()):
            imgPath = ':src="'+ f"atributes.atr{cssclass}" +'"'
        doesImageExist(elem.getimgpath(),elem,projectname)
        return ("<"+elem.tag +f" {ref}class="+'"grid-item-'+ idcomponent + ' container'+ cssclass + '" ' + imgPath +f' alt="container{cssclass}" '+ ' '.join(d for d in directives) , "/>")
    
    if(isinstance(elem, VectorElement)):
        generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
        doesImageExist(elem.getsvgpath(),elem,projectname)
        return ("<"+elem.tag +f" {ref}class="+'"grid-item-'+idcomponent+' container'+ cssclass + '" '+ 'src="' + elem.getsvgpath() + '"' +f' alt="container{cssclass}" '+ ' '.join(d for d in directives) , "/>")

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

    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="DatePicker"):
        useDatePickerPrimevuePlugin(projectname)
        cssclass= "sdatepicker" + cssclass
        vmodel = 'v-model="'+str(elem.vmodel)+'"'
        generateDatePickerCssProperties(projectname,pagename,cssclass,elem)
        componentAssets[pagename].extend([" DatePicker"])
        showicon = ""
        if(elem.style.getdropdownbackgroundcolor()!=None):
            showicon = ":showOnFocus='false' showIcon='' fluid=''"
        return (f'<DatePicker {id}{ref}{vmodel} class="{cssclass}" {showicon} >','</DatePicker>')
    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="Dropdown"):
        useSelectVuetifyPlugin(projectname)
        options = ':items="allOptionValues'+str(cssclass)+'"'
        cssclass= "svueselect" + cssclass
        vmodel = 'v-model="'+str(elem.vmodel)+'"'
        placeholder = 'label="'+str(elem.placeholder)+'"'
        generateVueSelectCssProperties(projectname,pagename,cssclass,elem)
        return (f"<v-select {id}{ref}class="+'"grid-item '+ cssclass  + '" :single-line="true" '+vmodel+' '+options+' '+placeholder, "/>")
    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="Form"):
        useFormPrimeVuePlugin(projectname)
        useToastPrimeVuePlugin(projectname)
        form = getPrimeVueForm(elem,cssclass,elem.inputs,elem.buttontxt)
        generateFormCssProperties(projectname,pagename,cssclass,elem,f"form{cssclass}",f"inputform{cssclass}",f"submitbtnform{cssclass}")
        auxiliarImports[pagename].add("import { ref } from 'vue'")
        auxiliarImports[pagename].add('import { useToastStore } from "@/stores/toast";')
        componentAssets[pagename].extend([" Form"," InputText"," Message"])
        return form
    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="Table"):
        useDataTablePrimevuePlugin(projectname)
        table = getPrimeVueDataTable(elem,cssclass)
        generateTableCssProperties(projectname,pagename,"stable"+cssclass,elem)
        componentAssets[pagename].extend([" DataTable"," Column"])
        return table
    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="Slider"):
        useSliderPrimevuePlugin(projectname)
        cssclass= "sslider" + cssclass
        vmodel = 'v-model="'+str(elem.vmodel)+'"'
        generateSliderCssProperties(projectname,pagename,cssclass,elem)
        componentAssets[pagename].extend([" Slider"])
        return (f'<Slider {id}{ref}{vmodel} class="{cssclass}" >','</Slider>')
    if(isinstance(elem, Mcomponent) and elem.getNameComponent()=="Paginator"):
        usePaginatorVuetifyPlugin(projectname)
        cssclass= "spaginator" + cssclass
        vmodel = 'v-model="'+str(elem.vmodel)+'"'
        generatePaginatorCssProperties(projectname,pagename,cssclass,elem)
        componentAssets[pagename].extend([" v-pagination"])
        return (f'<v-pagination {id}{ref}{vmodel} :total-visible="{elem.totalvisible}" :length="{elem.length}" class="{cssclass}" >','</v-pagination>')
    if(elem.getNameComponent()=="Checkbox" and elem.getTypeComponent()=="COMPONENT_ASSET"):
        useCheckboxPrimeVuePlugin(projectname)
        checkbox = getPrimeVueCheckbox(elem,cssclass)
        cssclass= "scheckbox" + cssclass
        generateCheckboxCssProperties(projectname,pagename,cssclass,f"label{cssclass}",elem)
        componentAssets[pagename].extend([" Checkbox"])
        return checkbox
    if(isinstance(elem, Mcomponent) and elem.getisVariant()==True):
        component = getFormatedName("Variant"+elem.getVariantName().lower().capitalize())
        nestedComponents.setdefault(pagename, {}).add(component)
        compbegin = f"""<{component} """+' '.join(d for d in directives) + f''' :variant="currentVariant{cssclass}"'''+f''' :componentprops="'''+f"selectedClass{cssclass}"+ '">'
        compend = f"""</{component}>"""
        return (compbegin,compend)
    if(isinstance(elem, Mcomponent)):
        componentName = getFormatedName(elem.getNameComponent().capitalize())
        classname = ' class="'+"grid-item-"+getElemId(elem.getIdComponent())+' component'+ getElemId(elem.getIdComponent())    
        if(elem.style.getPosition()!=None):
            classname += " pos"+componentName.lower()
            setComponentPositionCSS(projectname,pagename,"pos"+componentName.lower(),elem)
        nestedComponents.setdefault(pagename, {}).add(getFormatedName(elem.getNameComponent().lower()))
        return ("<"+componentName+f"{ref}{classname}"+'" '+ ' '.join(d for d in directives) + ">","</"+componentName+">")

    return ("","")

def writeVueComponent(name,project_name,content,component,pagesInfo):
    global allhooks, componentMethods
    componentMethods[name] = []
    componentsimports="\n"
    for comp in nestedComponents[name]:
        componentsimports += "import "+getFormatedName(str(comp).capitalize())+" from '@/components/"+getFormatedName(str(comp).capitalize())+".vue';\n" 
    for auximports in auxiliarImports[name]:
        componentsimports += auximports+";\n"
    cssimport = "@import '../assets/"+getFormatedName(name.lower())+".css';"
    pagehooks=""
    pagecomponents = "\n"
    allcomponents = (x.capitalize() for x in nestedComponents[name])
    allcomponents = list(allcomponents)
    if(len(allcomponents)>0): pagecomponents="""\n    components:{\n        """+ ',\n        '.join(allcomponents) +"""\n    },"""
    for hook in allhooks[name]:
        if("methods" in hook or "computed" in hook or "watch" in hook): pagehooks += hook + ":{\n"
        if("mounted" in hook or "destroyed" in hook or "setup" in hook or "beforeUnmount" in hook or "created" in hook):
            pagehooks += hook + "(){\n"
        if("methods" in hook and getKeyEventsFunction(name)!=None):
            pagehooks+=getKeyEventsFunction(name)+","
        for chook in allhooks[name][hook]:
            if("methods" in hook and chook[1] not in componentMethods[name]):
                pagehooks += chook[1] + ",\n"
                componentMethods[name].append(chook[1])               
            if("computed" in hook or "watch" in hook): 
                pagehooks += chook[1] + ",\n"
            if("mounted" in hook or "setup" in hook or "destroyed" in hook or "beforeUnmount" in hook or "created" in hook): 
                pagehooks += chook[1] + "\n\n"
        if(hook=="setup"):
            pagehooks+="        return {\n          """
            for c in allhooks[name][hook]:
                for retstatement in c[0]:
                    pagehooks += "  "+retstatement + ",\n          "
            pagehooks += "}\n\n"
        pagehooks=pagehooks[:-2]+"\n\t},"
    pagehooks = pagehooks[:-1]
    if(len(pagehooks)>0): pagehooks = ",\n    "+pagehooks
    template = '<div>'+ content + '</div>' #'<div class="grid-item-'+idcomponent+' component'+ idcomponent +'"'+ ">"+ content + '</div>'
    props =""
    if(component.getProps()!={}):
        props = """\n    props:{
        atributes: Object
    },"""
    componentpage = """<template>\n""" + processTemplate(template,name) + """
</template>
    
<script>"""+ componentsimports +"""export default {"""+ pagecomponents +f"""{props}"""+"""
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
        if(tag=="InputText"):
            processedTemplate = re.sub('<InputText'+r" ([\s]*.*?)"+'fluid=""'+r'([\s]*.*?)'+'>',"<InputText"+r" \1 fluid \2>",processedTemplate)
        if(tag=="Form"):
            processedTemplate = re.sub('<Form'+r" ([\s]*.*?)"+':initialvalues'+r'([\s]*.*?)'+':validateonblur'+r'([\s]*.*?)'+'>',"<Form"+r" \1 :initialValues\2 :validateOnBlur\3>",processedTemplate)
        finalHtml = processedTemplate
    finalHtml = re.sub('&amp;&amp;','&&',finalHtml)
    return finalHtml

def filterOverlapingElements(component,onstack):
    elements = component.getChildren()
    alllevelShapes = getShapes(elements)
    idel=-1
    idsh=-1
    if(len(alllevelShapes)>0):
        for s in alllevelShapes:
            idsh+=1
            for i in component.getChildren():
                idel+=1
                if(i!=s and idsh<idel and getValue(i.style.gridcolumnStart)>=getValue(s.style.gridcolumnStart) and
                    getValue(i.style.gridcolumnEnd)<=getValue(s.style.gridcolumnEnd) and
                    getValue(i.style.gridrowStart)>=getValue(s.style.gridrowStart) and
                    getValue(i.style.gridrowEnd)<=getValue(s.style.gridrowEnd) and
                    (isinstance(s,ShapeElement))):
                        onstack.append((i,s))
                for c in i.getChildren():
                    if(len(c.getChildren())>0): filterOverlapingElements(c,onstack)
    return onstack

def getShapes(elementos):
    return list(filter(lambda x: (isinstance(x,ShapeElement)),elementos))

def handleClipPathOverlaping(elementos):
    global pagename,globalprojectname
    repeatedElements = []
    for i, elem2 in enumerate(elementos):
        for j, elem1 in enumerate(elementos):
            if j>i:
                if (getValue(elem1.style.gridcolumnStart) >= getValue(elem2.style.gridcolumnStart) and
                    getValue(elem1.style.gridcolumnEnd) <= getValue(elem2.style.gridcolumnEnd) and
                    getValue(elem1.style.gridrowStart) >= getValue(elem2.style.gridrowStart) and
                    getValue(elem1.style.gridrowEnd) <= getValue(elem2.style.gridrowEnd) and
                    isinstance(elem2,ShapeElement) and j not in repeatedElements):
                    
                    if(isinstance(elem1,ShapeElement) and elem1.getType()=="LINE" and elem2.getType()=="LINE"): 
                        continue
                    updatePosition(elem1)
                    if(isinstance(elem1, Mcomponent) and elem1.getisVariant()==True):
                        updateZIndex(globalprojectname,pagename,elem1,1)
                    elem1.style.setGridcolumnStart(1)
                    elem1.style.setGridcolumnEnd(64)                    

                    elem2.getChildren().append(elem1)
                    elem2.style.setDisplay("grid")
                    repeatedElements.append(j)

    for index in sorted(set(repeatedElements), reverse=True):
        del elementos[index]

    for c in elementos:
        if(len(c.getChildren())>0):
            handleClipPathOverlaping(c.getChildren())
    
def flatTree(elementos):
    for node in elementos:
        yield node
        if node.getChildren():
            yield from flatTree(node.getChildren())

def anyShapes(elementos):
    allShapes = list(filter(lambda x: (isinstance(x,ShapeElement)),list(flatTree(elementos))))
    return len(allShapes) > 0

def updatePositions(component,variantComponents):
    for v in variantComponents:
        destIds = []
        for i in component.interactions:
            for a in i.actions:
                destIds.append(a.destinationID)
        if(component.style.gridcolumnStart==None and component.style.gridcolumnEnd==None and component.style.gridrowStart==None and component.style.gridrowEnd==None):
            for comp in variantComponents:
                if(comp.getNameComponent().count('=')==1 and comp.getNameComponent().split("=")[0]==component.getNameComponent().split("=")[0] and
                   comp.style.gridcolumnStart!=None and comp.style.gridcolumnEnd!=None and comp.style.gridrowStart!=None and comp.style.gridrowEnd!=None):
                    component.style.setGridcolumnStart(comp.style.gridcolumnStart)
                    component.style.setGridcolumnEnd(comp.style.gridcolumnEnd)
                    component.style.setGridrowStart(comp.style.gridrowStart)
                    component.style.setGridrowEnd(comp.style.gridrowEnd)                    
                if(comp.getNameComponent().split(",")[0] in component.getNameComponent() and comp.getNameComponent()!=component.getNameComponent()):
                    component.style.setGridcolumnStart(comp.style.gridcolumnStart)
                    component.style.setGridcolumnEnd(comp.style.gridcolumnEnd)
                    component.style.setGridrowStart(comp.style.gridrowStart)
                    component.style.setGridrowEnd(comp.style.gridrowEnd)

def getValue(value):
    if(value==None): return 0
    if(isinstance(value, int)): return value
    if(value.isnumeric()): return int(value)
    if(" span " in str(value)):
        realvalue = value.split(" span ")[1] 
        return int(realvalue)

def updatePosition(elem):
    if(elem.style.getGridcolumnEnd()>65):
        elem.style.setGridcolumnStart(elem.style.getGridcolumnStart()-15)
        elem.style.setGridcolumnEnd(elem.style.getGridcolumnEnd()-10)
    if(elem.style.getGridrowEnd()>65):
        elem.style.setGridrowStart(elem.style.getGridrowStart()-15)
        elem.style.setGridrowEnd(elem.style.getGridrowEnd()-10)    
        
def generateActionsAnimationStyle(projectname,pagename,cssclass,elem):
    for interaction in elem.getInteractions():
        for action in interaction.actions:
            if(action.getTransition()!=None):
                generateTransitionAnimation(projectname,pagename,cssclass,action.getTransition())
                
def insertTransitionComponent(element,output, endtag):
    global alltransitionodes
    if(getId(element) in alltransitionodes):
        output = '<Transition :name="animationName">'+ output 
        endtag = endtag + '</Transition>'
    return output, endtag