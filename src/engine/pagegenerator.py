from engine.stylegenerator import generatePageStyle, generateElemCssProperties
from parser.model.TextElement import TextElement
from parser.model.ContainerElement import ContainerElement
import xml.etree.ElementTree as ET

def buildpage(name,page):
    #build page root layout
    #writeVue(name,page)
    # build elements from the page  
    #print(page)
    output = ""  
    for element in page.elements:
        output += processChildren(element,name,page.pagename)
        #pretty_print_xml_elementtree(getHtml(element))
    #print(getIndentedXML(output))
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
    cssclass = elem.idElement.replace(":","")
    if isinstance(elem, TextElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'text'+ cssclass,elem)
            return ("<p class="+'"grid-item text'+ cssclass +'">'+elem.text, "</p>")
    if isinstance(elem, ContainerElement):
        if elem.tag=="" or elem.tag == None:
            generateElemCssProperties(projectname,pagename,'container'+ cssclass,elem)
            return ("<div class="+'"grid-item container'+ cssclass +'">', "</div>")

#still without elements
def writeVue(name,page,content):
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    template = '<div class="grid-container">'+ content + '</div>'
    vuepage = """<template>\n\t\t""" + getIndentedXML(template) + """
</template>

<script>
export default {
    data(){
        return {
        }
    },
    methods:{
    }
}
</script>
<style lang="css" scoped>
"""+ cssimport +"""
</style>"""
    with open("../output/"+name+"/src/views/"+page.getPagename()+"View.vue","w") as f:
        f.write(vuepage)
    generatePageStyle(name,page)


def indent(elem, level=1):
   indent_size = "  "
   i = "\n" + level * indent_size
   if len(elem):
      if not elem.text or not elem.text.strip():
         elem.text = i + indent_size
      if not elem.tail or not elem.tail.strip():
         elem.tail = i
      for elem in elem:
         indent(elem, level + 1)
      if not elem.tail or not elem.tail.strip():
         elem.tail = i
   else:
      if level and (not elem.tail or not elem.tail.strip()):
         elem.tail = i

def getIndentedXML(xml_string):

   root = ET.fromstring(xml_string)
   indent(root)

   indented_xml = ET.tostring(root, encoding="unicode",short_empty_elements=False)
   return indented_xml

