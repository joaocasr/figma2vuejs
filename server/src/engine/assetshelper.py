from utils.tools import getFormatedName,getElemId

def getPrimeVueForm(elem,formid,inputsinfo,buttontext):
    template = f'''
    <div class="form{formid}">
    <Form v-slot="$form{formid}" :initialValues="initialValues{formid}" :resolver="resolver{formid}" :validateOnBlur="true" @submit="onFormSubmit{formid}">
    '''
    nr_input = 0
    for minput in inputsinfo:
      nr_input+=1
      label = ""
      if("label" in minput):
        label=f'<label class="label{formid}" for="input{nr_input}{formid}">{minput["label"]["text"]}</label><br>'
      template+=f'''<div class="inputform{formid}">
                {label}
                <InputText id="input{nr_input}{formid}" name="input{nr_input}{formid}" type="text" placeholder="{minput["placeholder"]}" fluid />
                '''+f'''<Message v-if="'''+f'$form{formid}.input{nr_input}{formid}?.invalid" severity="error" size="small" variant="simple">'+'{{'+f'$form{formid}.input{nr_input}{formid}?.error.message'+'}}'+"""</Message> 
            </div>
            """
    template+=f'''<Button class="submitbtnform{formid}" type="submit" label="Submit">{buttontext}</Button>
    '''
    return (template,"</Form></div>")

def getPrimeVueCheckbox(elem,checkboxid):
    template = f'''<div class="scheckbox{checkboxid}">
        <div v-for="box of boxes{checkboxid}" :key="box.key">
                <Checkbox v-model="selectedCategories" :inputId="box.key" name="box" :value="box.name" />
                <label class="labelscheckbox{checkboxid}" :for="box.key">'''+'''{{ box.name }}'''+'''</label>
        </div>
    '''
    return (template,"</div>")


def getVuetifyMenu(elem,menuid,idcomponent=None):
    mclass=f"smenu{menuid}"
    if(idcomponent!=None):
        mclass="grid-item-"+idcomponent+" "+mclass
    template = f'''<div class="{mclass}'''+'''">
    <v-menu>
      <template v-slot:activator="'''+"{ props }"+'''">
        <div v-bind="props">
        '''
    if(elem.iconImage!=None):
      template+=f'''<img alt="{getFormatedName(elem.iconImage["name"])+getElemId(elem.iconImage["id"])}"
              src="/{getFormatedName(elem.iconImage["name"])+getElemId(elem.iconImage["id"])}.png"
            />
            '''
    template+=f'''   </div>
      </template>
      <v-list>
        <v-list-item v-for="(item, index) in menuoptions{menuid}" :key="index" :value="index">
          <v-list-item-title @click="selectedItem{menuid}(item)">'''+"{{ item.option }}"+'''</v-list-item-title>
        </v-list-item>
      </v-list>
    '''
    return (template,"</v-menu></div>")

def getPrimeVueDataTable(elem,tableid):
  template = f'''<DataTable class="stable{tableid}" :value="tablevalues{tableid}" :rows="{elem.nrrows}">'''
  for c in elem.header:
    if(elem.header[c]["type"]=="TEXT"): #handle different data types
      template+=f'''  <Column field="{elem.header[c]["name"]}" header="{elem.header[c]["name"].capitalize()}" style="width: 25%"></Column>
      '''
    if(elem.header[c]["type"]=="IMAGE"):
      template+=f'''   <Column header="{elem.header[c]["name"].capitalize()}">
        <template #body="{elem.header[c]["name"].capitalize()}">
            <img :src="`{elem.header[c]["name"]}.png`" style="width: 25%"/>
        </template>
    </Column>'''
  return (template,"</DataTable>")