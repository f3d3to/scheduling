import { createRouter, createWebHistory } from 'vue-router';
import HomePage from "../components/HomePage.vue";
import GraphContainer from '../components/GraphContainer.vue';
import Timer from '../components/Timer.vue';
import Planificadores from '../components/Planificadores.vue';
import Estados from "../components/Estados.vue";
import EstructuraPlanificador from "../components/EstructuraPlanificador.vue";
import Celda from "../components/Celda.vue";
import Mensajes from "../components/Mensajes.vue";
import Actividades from "../components/Actividades.vue";
import Tareas from "../components/Tareas.vue";
import Objetivos from "../components/Objetivos.vue";
import Etiquetas from "../components/Etiquetas.vue";
import Comentarios from "../components/Comentarios.vue";
import Recurrentes from "../components/Recurrentes.vue";
import Eventos from "../components/Eventos.vue";
import EventosAsociados from "../components/EventosAsociados.vue";
import Elementos from "../components/Elementos.vue";
import RegistroProgreso from "../components/RegistroProgreso.vue";

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/planes', name: 'Planeas', component: GraphContainer },
  { path: '/timer', name: 'Timer', component: Timer },
  { path: '/planificadores', name: 'Planificadores', component: Planificadores },
  { path: '/estados', name: 'Estados', component: Estados },
  { path: '/estructurasPlanificador', name: 'EstructuraPlanificador', component: EstructuraPlanificador },
  { path: '/celdas', name: 'Celda', component: Celda },
  { path: '/mensajes', name: 'Mensajes', component: Mensajes },
  { path: '/actividades', name: 'Actividades', component: Actividades },
  { path: '/tareas', name: 'Tareas', component: Tareas },
  { path: '/objetivos', name: 'Objetivos', component: Objetivos },
  { path: '/etiquetas', name: 'Etiquetas', component: Etiquetas },
  { path: '/comentarios', name: 'Comentarios', component: Comentarios },
  { path: '/recurrentes', name: 'Recurrentes', component: Recurrentes },
  { path: '/eventos', name: 'Eventos', component: Eventos },
  { path: '/eventosAsociados', name: 'EventosAsociados', component: EventosAsociados },
  { path: '/elementos', name: 'Elementos', component: Elementos },
  { path: '/registrosProgreso', name: 'RegistroProgreso', component: RegistroProgreso },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
