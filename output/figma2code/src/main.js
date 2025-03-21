import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import usePrimeVue from './plugins/primevue';

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(router)

usePrimeVue(app)


app.mount('#app')
