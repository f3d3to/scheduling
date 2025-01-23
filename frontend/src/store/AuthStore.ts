// Third-party
import { jwtDecode } from 'jwt-decode';
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Proyect
import { api, verifyToken } from '../services/apiServiceAuth';
import router from '../router';
// Stores
import { usePlansStore } from './PlanStore';
import { useGraphStore } from './GraphStore';
import { usePlanificadorStore } from './PlanificadorStore';
import { usePomodoroStore } from './PomodoroStore';


interface JwtPayload {
    user_id: number;
    username: string;
    exp: number;
    iat: number;
}

interface Usuario {
    id: number;
    username: string;
    email: string;
    perfil?: string;
}

export const useAuthStore = defineStore('auth', () => {
    // Estado
    const user = ref<Usuario | null>(null);
    const isAuthenticated = ref(false);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const redirectToLogin = () => {
        // Redirige al usuario a la página de login
        // Usa el enrutador de Vue para la navegación
        router.push('/login'); // Asume que tu ruta de login es '/login'
      };

    const login = async (credentials: { username: string; password: string }) => {
        isLoading.value = true;
        error.value = null;

        try {
            // Obtener tokens
            const response = await api.post('token/', credentials);
            // Verificar y decodificar token
            const isValid = await verifyToken(response.data.access);

            if (!isValid) throw new Error('Token inválido');

            // Almacenar tokens
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);

            // Obtener datos de usuario
            isAuthenticated.value = true;
            await fetchUser();

        } catch (err) {
            logout();
            error.value = (err as Error).message || 'Error de autenticación';
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    const fetchUser = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                logout();
                throw new Error("No se encontró token de acceso");
            }
            const decodedToken = jwtDecode<JwtPayload>(token)
            const user_id = decodedToken.user_id; // Obtiene el username del token
            // Buscar el usuario por username (asumiendo que tu API lo soporta)
            const response = await api.get(`usuarios/?id=${user_id}`);
            if (response.data.results.length > 0) {
                response.data
                user.value = response.data.results[0];
            } else {
                throw new Error('Usuario no encontrado');
            }
        } catch (err) {
            logout();
            throw err;
        }
    };

    const checkAuth = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        try {
            const isValid = verifyToken(token);

            if (isValid) {
                isAuthenticated.value = true;
                await fetchUser();
            } else {
                redirectToLogin();
                logout();
            }
        } catch (err) {
            logout();
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        user.value = null;
        isAuthenticated.value = false;
        error.value = null;
    };

    // Inicialización
    const initialize = async () => {
        await checkAuth();
        if (!isAuthenticated.value) {
          redirectToLogin();
        }
        await initializeDependentStores();

    };

    return {
        user,
        isAuthenticated,
        isLoading,
        redirectToLogin,
        error,
        login,
        logout,
        fetchUser,
        checkAuth,
        initialize
    };
});

const initializeDependentStores = async () => {
    const graphStore = useGraphStore();
    const plannerStore = usePlanificadorStore();
    const pomodoroStore = usePomodoroStore();

    await pomodoroStore.fetchSessions();
    await pomodoroStore.fetchTasks();
    await pomodoroStore.fetchActividades();




};
