import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importa el router configurado
import './style.css'; // Importa estilos globales si los tienes

const app = createApp(App);

app.use(router); // Usa el router
app.mount('#app');
