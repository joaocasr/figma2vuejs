from utils.processing import getFormatedName,getElemId,doesImageExist

def writeVariantComponent(name,project_name,variants):

    template = """<template >
    <component :is="selectedComponent" v-bind="componentProps" :key="variant"></component>
</template>
  
<script>
"""
    for comp in variants:
        template += "import "+getFormatedName(str(comp.getNameComponent()).capitalize())+" from '@/components/"+getFormatedName(str(comp.getNameComponent()).capitalize())+".vue';\n" 
    template += """  export default {
    props: {
      variant: {
        type: String,
        required: true,
        validator: (value) => [
"""
    for comp in variants:
        template+="""            '"""+getFormatedName(str(comp.getNameComponent())).lower()+"""',\n"""
        
    template=template[:-2]+"""].includes(value),
      },
      componentProps: {
        type: Object,
        default: () => ({}),
      },
    },
    computed: {
      selectedComponent() {
          
""" 
    for comp in variants:
        template+="""        if(this.variant ==='"""+getFormatedName(str(comp.getNameComponent())).lower()+"""'){
          this.variant = """+getFormatedName(str(comp.getNameComponent())).capitalize()+""";
        }
"""
    
    template+="""
        return this.variant;
      },
    }
  };
  </script>
    """
    with open("../output/"+project_name+"/src/components/Variant"+getFormatedName(name.lower())+".vue","w") as f:
        f.write(template)