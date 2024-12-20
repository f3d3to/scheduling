import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import router from './router';
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css' // Iconos Material Design
import 'vuetify/styles' // Estilos de Vuetify

// Importar componentes y directivas de Vuetify (opcional si los usas explícitamente)
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Crear instancia de Vuetify
const vuetify = createVuetify({
  components, // Registro explícito de componentes
  directives, // Registro explícito de directivas
  ssr: true, // Server-Side Rendering si es necesario
})

// Crear y montar la app
const app = createApp(App)
app.use(vuetify)

app.use(router);

app.mount('#app')
