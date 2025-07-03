from utils.tools import getFormatedName,getElemId,doesImageExist

def writeVariantComponent(name,project_name,variants):
    template = """<template >
    <component :is="selectedComponent" :class="componentprops" :key="variant"></component>
</template>
  
<script>
"""
    for comp in variants:
      template += "import "+getFormatedName(str(comp.getNameComponent()).capitalize())+" from '@/components/"+getFormatedName(str(comp.getNameComponent()).capitalize())+".vue';\n" 
    template+="""
const componentsMap = {
"""
    for comp in variants:
      template+=getFormatedName(str(comp.getNameComponent())).lower()+":"+getFormatedName(str(comp.getNameComponent())).capitalize()+",\n"
    if(len(variants)==0): template+= "};\n"
    else: template = template[:-2] + "};\n"
    template += """export default {
    props: {
      variant: {
        type: String,
        required: true,
        validator: (value) => [
"""
    for comp in variants:
        template+="""            '"""+getFormatedName(str(comp.getNameComponent())).lower()+"""',\n"""
      
    if(len(variants)==0): template+= """].includes(value),
      },
      componentprops: {
        type: String,
        required: true,
        default: '',
      },
    },
    computed: {
      selectedComponent() {"""
    else: template=template[:-2]+"""].includes(value),
      },
      componentprops: {
        type: String,
        required: true,
        default: '',
      },
    },
    computed: {
      selectedComponent() {""" 

    
    template+="""
        return componentsMap[this.variant];
      },
    }
  };
  </script>
    """
    with open("../output/"+project_name+"/src/components/Variant"+getFormatedName(name.lower())+".vue","w") as f:
        f.write(template)