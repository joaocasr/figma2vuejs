import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css';
import { VRating } from 'vuetify/components';

const vuetify = createVuetify({
components: {
	VRating
},
icons: {
defaultSet: 'mdi',
}
})

export default vuetify;
