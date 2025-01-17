import { createRouter, createWebHistory } from 'vue-router';

// Importaciones usando rutas relativas
import HomePage from '../components/common/HomePage.vue';
import GraphContainer from '../components/views/planes/GraphContainer.vue';
import Timer from '../components/views/timer/Timer.vue';
import Planificadores from '../components/views/dashboards/Planificadores.vue';
import PlanificadorDetalle from '../components/views/planificador/detalles/PlanificadorDetalle.vue';
import IniciarSesion from '../components/views/users/Login.vue'
import RegistroUsuario from '../components/views/users/RegistroUsuario.vue'
import PerfilUsuario from '../components/views/users/PerfilUsuario.vue'
import EditarPerfil from '../components/views/users/EditarPerfil.vue'


const routes = [
  { path: '/', name: 'Home', component: HomePage },
  {
    path: '/planificador/:id',
    name: 'PlanificadorDetalle',
    component: PlanificadorDetalle,
    props: true,
  },
  { path: '/iniciar-sesion', name: 'Login', component: IniciarSesion },
  { path: '/registro', name: 'RegistroUsuario', component: RegistroUsuario },
  { path: '/mi-perfil', name: 'PerfilUsuario', component: PerfilUsuario },
  { path: '/editar-mi-perfil', name: 'EditarPerfil', component: EditarPerfil },

  { path: '/planes', name: 'Planes', component: GraphContainer },
  { path: '/timer', name: 'Timer', component: Timer },
  { path: '/planificadores', name: 'Planificadores', component: Planificadores },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
