import { createRouter, createWebHistory } from 'vue-router';
import Timer from '../components/Timer.vue';
import GraphContainer from '../components/GraphContainer.vue';
import Planificadores from '../components/Planificadores.vue';
import HomePage from "../components/HomePage.vue";

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/planes', name: 'Planeas', component: GraphContainer },
  { path: '/timer', name: 'Timer', component: Timer },
  { path: '/planificadores', name: 'Planificadores', component: Planificadores },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
