import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { plugin, defaultConfig } from '@formkit/vue';

import { createPinia } from 'pinia';

import { createApp } from 'vue'
import router from './router';
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createNotivue } from 'notivue'

import 'notivue/notification.css' // Only needed if using built-in notifications
import 'notivue/animations.css' // Only needed if using built-in animations

const pinia = createPinia();
const notivue = createNotivue({position: 'top-right'})
const vuetify = createVuetify({
  components,
  directives,
  ssr: true,
})

const app = createApp(App)
app.use(pinia);
app.use(notivue);
app.use(plugin, defaultConfig())
app.use(VueSweetalert2);
app.use(vuetify)
app.use(router);
app.mount('#app')
