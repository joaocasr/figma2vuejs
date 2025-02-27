from engine.stylegenerator import generatePageStyle, generateElemCssProperties
from engine.logicgenerator import handleBehaviour
from parser.model.TextElement import TextElement
from parser.model.ContainerElement import ContainerElement
import xml.etree.ElementTree as ET
from lxml import etree, html

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
    # build elements from the page  
    output = ""  
    for element in page.elements:
        output += processChildren(element,name,page.pagename)

    writeVue(name,page,output)

def processChildren(data,projectname,pagename):
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
    global allPagesInfo, allhooks
    cssclass = elem.idElement.replace(":","")
    if isinstance(elem, TextElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
            #iterate the list of interactions (logicgenerator.py)
            return ("<p class="+'"grid-item text'+ cssclass +'">'+elem.text, "</p>")
    if isinstance(elem, ContainerElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
            #iterate the list of interactions (logicgenerator.py)
            directives, hooks = handleBehaviour(elem,cssclass,allPagesInfo)
            if(hooks!=None): 
                for hook in hooks:
                    allhooks[pagename].setdefault(hook, []).extend(hooks[hook])
            html = "<div class="+'"grid-item container'+ cssclass + '" '+ ' '.join(d for d in directives) +">"
            return (html, "</div>")

#still without elements
def writeVue(name,page,content):
    global allhooks
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    template = '<div class="grid-container">'+ content + '</div>'

#',\n\t\t'.join(str(allhooks[page.getPagename()][hook]) for hook in allhooks[page.getPagename()]) + """
    pagehooks=""
    for hook in allhooks[page.getPagename()]:
        pagehooks = hook + ":{\n"
        for content in allhooks[page.getPagename()][hook]:
            pagehooks += content + ",\n"
        pagehooks = pagehooks[:-2]
        pagehooks +="\n\t}"
    vuepage = """<template>\n""" + getIndentedHTML(template) + """
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
    with open("../output/"+name+"/src/views/"+page.getPagename()+"View.vue","w") as f:
        f.write(vuepage)
    generatePageStyle(name,page)


def getIndentedHTML(html_string):
    myhtml = html.fromstring(html_string)
    etree.indent(myhtml, space="    ")
    return etree.tostring(myhtml, encoding='unicode', pretty_print=True)

