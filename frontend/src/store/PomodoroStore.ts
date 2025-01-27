import { defineStore } from 'pinia';
import { ref, computed, onMounted } from 'vue';
import { api } from '../services/apiServiceAuth';

// Función de ayuda para cargar desde localStorage
const loadState = <T>(key: string, defaultValue: T): T => {
  try {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : defaultValue;
  } catch {
    return defaultValue;
  }
};

export const usePomodoroStore = defineStore('pomodoro', () => {
  // Estado central con persistencia
  const sessions = ref<any[]>([]);
  const tasks = ref<any[]>([]);
  const actividades = ref<any[]>([]);

  // Estados persistentes
  const selectedSession = ref<any>(loadState('selectedSession', {}));
  const selectedTask = ref<any>(loadState('selectedTask', null));
  const timer = ref(loadState('timer', 60 * 60));
  const timerRunning = ref(loadState('timerRunning', false));
  const interval = ref<any>(null);

  // Tiempo de inicio para calcular el tiempo restante
  const startTime = ref(loadState<number | null>('startTime', null));

  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // TO-DO :
  // Restaurar timer si estaba corriendo
  // onMounted(() => {
  //   if (timerRunning.value && startTime.value) {
  //     const elapsed = Math.floor((Date.now() - startTime.value) / 1000);
  //     const remaining = timer.value - elapsed;
  //     timer.value = remaining > 0 ? remaining : 0;

  //     if (remaining > 0) {
  //       startTimer();
  //     } else {
  //       handleTimerEnd();
  //     }
  //   }
  // });

  // Guardar estado en localStorage cuando cambia
  const saveState = () => {
    const state = {
      selectedSession: selectedSession.value,
      selectedTask: selectedTask.value,
      timer: timer.value,
      timerRunning: timerRunning.value,
      startTime: timerRunning.value ? Date.now() : null
    };

    Object.entries(state).forEach(([key, value]) => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  };

  // Modificar las acciones para incluir saveState()
  const startTimer = () => {
    if (!timerRunning.value) {
      timerRunning.value = true;
      startTime.value = Date.now();
      interval.value = setInterval(() => {
        if (timer.value > 0) {
          timer.value--;
          saveState();
        } else {
          handleTimerEnd();
        }
      }, 1000);
      saveState();
    }
  };

  const pauseTimer = () => {
    timerRunning.value = false;
    startTime.value = null;
    clearInterval(interval.value);
    saveState();
  };

  const resetTimer = () => {
    timerRunning.value = false;
    startTime.value = null;
    clearInterval(interval.value);
    timer.value = selectedSession.value.duracion_minutos
      ? selectedSession.value.duracion_minutos * 60
      : 60 * 60;
    saveState();
  };

  const selectSession = (session: any) => {
    selectedSession.value = session;
    timer.value = session.duracion_minutos * 60;
    saveState();
  };

  const deselectSession = () => {
    selectedSession.value = {};
    resetTimer();
    saveState();
  };

  const selectTask = (task: any) => {
    selectedTask.value = task;
    saveState();
  };

  const deselectTask = () => {
    selectedTask.value = null;
    saveState();
  };

  const formattedTime = computed(() => {
    const minutes = Math.floor(timer.value / 60);
    const seconds = timer.value % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  });

  // Limpiar localStorage cuando el timer termina
  const handleTimerEnd = async () => {
    clearInterval(interval.value);
    timerRunning.value = false;
    startTime.value = null;

    if (selectedTask.value) {
      selectedTask.value.cantidad_completadas++;
      await updateTask(selectedTask.value);
    }

    // Limpiar solo los datos del timer
    ['timer', 'timerRunning', 'startTime'].forEach(key => {
      localStorage.removeItem(key);
    });

    resetTimer();
  };
  // CRUD Sesiones
  const createSession = async (sessionData: any) => {
    try {
      const response = await api.post('sesiones/', sessionData);
      sessions.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  };

  const updateSession = async (sessionData: any) => {
    try {
      const response = await api.patch(`sesiones/${sessionData.id}/`, sessionData);
      const index = sessions.value.findIndex(s => s.id === sessionData.id);
      if (index !== -1) sessions.value.splice(index, 1, response.data);
        return response.data;
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await api.delete(`sesiones/${sessionId}/`);
      sessions.value = sessions.value.filter(s => s.id !== sessionId);
      if (selectedSession.value?.id === sessionId) {
        selectedSession.value = {};
        resetTimer();
      }
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  };

  // CRUD Tareas
  const createTask = async (taskData: any) => {
    try {
      const payload = {
        cantidad_completadas: taskData.cantidad_completadas,
        cantidad_para_completar: taskData.cantidad_para_completar,
        actividad_id: taskData.actividadId,

        tarea: {
          nombre: taskData.nombre,
          actividad_id: taskData.actividadId,
          descripcion: taskData.descripcion,
          color: taskData.color,
          fecha_limite: taskData.fecha_limite
        }
      };
      const response = await api.post('tareasTimer/', payload);
      tasks.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  };
  const updateTask = async (taskData: any) => {
    try {
      const payload = {
        cantidad_completadas: taskData.cantidad_completadas,
        cantidad_para_completar: taskData.cantidad_para_completar,
        tarea: {
          nombre: taskData.nombre,
          descripcion: taskData.descripcion,
          actividad: taskData.actividadId,
          color: taskData.color,
          fecha_limite: taskData.fecha_limite
        }
      };

      const response = await api.put(`tareasTimer/${taskData.id}/`, payload);

      const index = tasks.value.findIndex(t => t.id === taskData.id);
      if (index !== -1) {
        tasks.value.splice(index, 1, {
          ...response.data,
          nombre: response.data.tarea.nombre,
          descripcion: response.data.tarea.descripcion,
          actividad: response.data.tarea.actividad.nombre
        });
      }

      return response.data;
    } catch (err) {
      error.value = err.message;
      throw err;
    }
  };

 // Acciones
 const fetchSessions = async () => {
    isLoading.value = true;
    try {
      const response = await api.get('sesiones/');
      sessions.value = response.data.results || [];
    } catch (err) {
      error.value = err.message;
      console.error('Error fetching sessions:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchTasks = async () => {
    isLoading.value = true;
    try {
      const response = await api.get('tareasTimer/');
      tasks.value = response.data.results.map((task: any) => ({
        ...task,
        id: task.id,
        nombre: task.tarea.nombre,
        descripcion: task.tarea.descripcion,
        actividad: task.tarea.actividad.nombre,
      }));
    } catch (err) {
      error.value = err.message;
      console.error('Error fetching tasks:', err);
    } finally {
      isLoading.value = false;
    }
  };

  const fetchActividades = async () => {
    try {
      const response = await api.get('actividades/');
      actividades.value = response.data.results || [];
    } catch (err) {
      error.value = err.message;
      console.error('Error fetching activities:', err);
    }
  };

  return {
    // Estado
    sessions,
    tasks,
    actividades,
    selectedSession,
    selectedTask,
    timerRunning,
    isLoading,
    error,

    // Getters
    formattedTime,

    // Acciones
    fetchSessions,
    fetchTasks,
    fetchActividades,
    startTimer,
    pauseTimer,
    resetTimer,
    createSession,
    updateSession,
    deleteSession,
    createTask,
    updateTask,
    selectSession,
    deselectSession,
    selectTask,
    deselectTask
  };
});