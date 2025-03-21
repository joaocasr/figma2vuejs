import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';
import InputText from 'primevue/inputtext';
import InputIcon from 'primevue/inputicon';
import IconField from 'primevue/iconfield';


export default function usePrimeVue(app){

app.use(PrimeVue, {
theme: {
preset: Material
}
});
app.component('InputText',InputText)
app.component('InputIcon',InputIcon)
app.component('IconField',IconField)

}
