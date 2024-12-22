import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import router from './router';
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  ssr: true,
})

const app = createApp(App)
app.use(vuetify)

app.use(router);

app.mount('#app')
