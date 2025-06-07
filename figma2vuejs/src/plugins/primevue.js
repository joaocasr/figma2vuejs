import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import 'primeicons/primeicons.css';
import Toast from 'primevue/toast';
import { Form } from '@primevue/forms';
import InputText from 'primevue/inputtext';
import Message from 'primevue/message';
import ProgressBar from 'primevue/progressbar';

export default function usePrimeVue(app){

app.use(PrimeVue, {
theme: {
preset: Material
}
});
app.component('Toast',Toast);
app.component('Form',Form)
app.component('InputText',InputText)
app.component('Message',Message)
app.component('ProgressBar',ProgressBar)

}
