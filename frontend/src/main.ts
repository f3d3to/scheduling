import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import { createApp } from 'vue'
import router from './router';
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'



const vuetify = createVuetify({
  components,
  directives,
  ssr: true,
})

const app = createApp(App)
app.use(VueSweetalert2);
app.use(vuetify)

app.use(router);

app.mount('#app')
