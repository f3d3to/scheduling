import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/AuthStore';

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
import CalendarioAcademicoDashboard from '../components/views/calendario-academico/CalendarioAcademico.vue'
import CrearPlan from '../components/views/planes/CrearPlan.vue';


const routes = [
  { path: '/', name: 'Home', component: HomePage, meta: { requiresAuth: true },},
  {
    path: '/planificador/:id',
    name: 'PlanificadorDetalle',
    component: PlanificadorDetalle,
    props: true,
  },
  { path: '/login', name: 'Login', component: IniciarSesion },
  { path: '/registro', name: 'RegistroUsuario', component: RegistroUsuario },
  { path: '/mi-perfil', name: 'PerfilUsuario', component: PerfilUsuario },
  { path: '/editar-mi-perfil', name: 'EditarPerfil', component: EditarPerfil },

  { path: '/crear-plan', name: 'CrearPlan', component: CrearPlan },

  { path: '/calendario/academico', name: 'CalendarioAcademico', component: CalendarioAcademicoDashboard },
  { path: '/planes', name: 'Planes', component: GraphContainer },
  { path: '/timer', name: 'Timer', component: Timer },
  { path: '/planificadores', name: 'Planificadores', component: Planificadores },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado
    next('/login'); // Redirige al login
  } else {
    next(); // Continúa con la navegación
  }
});

export default router;
