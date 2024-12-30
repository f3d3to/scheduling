import { createRouter, createWebHistory } from 'vue-router';

// Importaciones usando rutas relativas
import HomePage from '../components/common/HomePage.vue';
import GraphContainer from '../components/views/planes/GraphContainer.vue';
import Timer from '../components/views/timer/Timer.vue';
import Planificadores from '../components/views/dashboards/Planificadores.vue';
import Estados from '../components/views/cruds/Estados.vue';
import EstructuraPlanificador from '../components/views/cruds/EstructuraPlanificador.vue';
import Celda from '../components/views/cruds/Celda.vue';
import Mensajes from '../components/views/cruds/Mensajes.vue';
import Actividades from '../components/views/cruds/Actividades.vue';
import Tareas from '../components/views/cruds/Tareas.vue';
import Objetivos from '../components/views/cruds/Objetivos.vue';
import Etiquetas from '../components/views/cruds/Etiquetas.vue';
import Comentarios from '../components/views/cruds/Comentarios.vue';
import Recurrentes from '../components/views/cruds/Recurrentes.vue';
import Eventos from '../components/views/cruds/Eventos.vue';
import EventosAsociados from '../components/views/cruds/EventosAsociados.vue';
import Elementos from '../components/views/cruds/Elementos.vue';
import RegistroProgreso from '../components/views/cruds/RegistroProgreso.vue';
import PlanificadorDetalle from '../components/views/planificador/detalles/PlanificadorDetalle.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  {
    path: '/planificador/:id',
    name: 'PlanificadorDetalle',
    component: PlanificadorDetalle,
    props: true,
  },
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
