import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css';
import { VPagination } from 'vuetify/components';
import { VRating } from 'vuetify/components';

const vuetify = createVuetify({
components: {
	VPagination,
VRating
},
icons: {
defaultSet: 'mdi',
}
})

export default vuetify;
