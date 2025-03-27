import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';
import Checkbox from 'primevue/checkbox';
import { Form } from '@primevue/forms';
import Message from 'primevue/message';
import InputText from 'primevue/inputtext';
import InputIcon from 'primevue/inputicon';
import IconField from 'primevue/iconfield';


export default function usePrimeVue(app){

app.use(PrimeVue, {
theme: {
preset: Material
}
});
app.component('Checkbox',Checkbox)
app.component('Form',Form)
app.component('Message',Message)
app.component('InputText',InputText)
app.component('InputIcon',InputIcon)
app.component('IconField',IconField)

}
