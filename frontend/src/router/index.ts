import { createRouter, createWebHistory } from 'vue-router';
import Timer from '../components/Timer.vue'; // Importa el componente Timer
import GraphContainer from '../components/GraphContainer.vue'; // Otro ejemplo

const routes = [
  { path: '/', name: 'Home', component: GraphContainer },
  { path: '/timer', name: 'Timer', component: Timer }, // Ruta para el temporizador
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
