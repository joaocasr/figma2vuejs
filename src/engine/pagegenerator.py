from engine.stylegenerator import generatePageStyle

def buildpage(name,page):
    #build page root layout
    #print(page)
    writeVue(name,page)
    #build elements from the page    
    #for element in page.elements:
        #processChildren(element.getIdElement(),element)
        #pretty_print_xml_elementtree(getHtml(element))

def processChildren(name,data):

    if(len(data.children)>0):
        for element in data.children:

            elem = processChildren(element.getIdElement(),element)
            #getHtml(elem)
            pretty_print_xml_elementtree(getHtml(elem))

#def getHtml(elem):
#    print(">>>>")
#    print(elem)

#still without elements
def writeVue(name,page):
    cssimport = "@import '../assets/"+page.getPagename().lower()+".css';"
    vuepage = """<template>
    <div class="grid-container">
    
    </div>
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


def indent(elem, level=0):
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

def pretty_print_xml_elementtree(xml_string):

   root = ET.fromstring(xml_string)
   indent(root)

   pretty_xml = ET.tostring(root, encoding="unicode")
   print(pretty_xml)

