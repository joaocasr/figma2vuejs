from utils.processing import getFormatedName,getElemId

def getPrimeVueForm(elem,formid,inputsinfo,buttontext):
    template = f'''
    <div class="form{formid}">
    <Form v-slot="$form{formid}" :initialValues="initialValues{formid}" :resolver="resolver{formid}" :validateOnBlur="true" @submit="onFormSubmit{formid}">
    '''
    for minput in inputsinfo:
        template+=f'''<div class="inputform{formid}">
                <InputText name="{minput["name"]}" type="text" placeholder="{minput["placeholder"]}" fluid />
                '''+f'''<Message v-if="'''+f'$form{formid}.{minput["name"]}?.invalid" severity="error" size="small" variant="simple">'+'{{'+f'$form{formid}.{minput["name"]}?.error.message'+'}}'+"""</Message> 
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
    template+=f'''<img
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
