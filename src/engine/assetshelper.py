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