<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card :style="{ backgroundColor: selectedSession.color || '#dbd9d9', color: '#fff' }"
        >
          <v-card-title class="text-center">Pomodoro </v-card-title>
          <v-card-title class="text-center" v-if="selectedSession">
            <strong>{{ selectedSession.nombre }}</strong>
            <v-icon
              v-if="selectedSession.id"
              class="icono-deseleccionar"
              size="25px"
              @click="deseleccionarSesion"
              title="Desmarcar sesión"
            >
              mdi-close
            </v-icon>
          </v-card-title>
          <v-card-text class="text-center display-1 font-weight-bold">
            {{ formattedTime }}
          </v-card-text>

          <v-card-text class="text-center" v-if="selectedTask">
            <strong>{{ selectedTask.nombre }}</strong>
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="startTimer" :disabled="timerRunning" prepend-icon="mdi-play">
              Iniciar
            </v-btn>
            <v-btn color="warning" @click="pauseTimer" :disabled="!timerRunning" prepend-icon="mdi-pause">
              Pausa
            </v-btn>
            <v-btn color="error" @click="resetTimer" prepend-icon="mdi-stop">Reiniciar</v-btn>
          </v-card-actions>

          <v-card-actions class="justify-center">
            <v-btn color="secondary" @click="manageSessionsDialog = true" >
              <v-icon size="25px">mdi-dots-horizontal</v-icon>
              Sesiones
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-4" >
      <v-col cols="12" md="8">
        <v-card-title v-if="tasks.length > 0" >Tareas
        <v-btn
          color="primary"
          @click="showAddTaskDialog"
          class="mb-2"
          v-if="tasks.length > 0"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-card-title>
        <div v-show="tasks.length > 0" >
          <v-card
            v-for="task in tasks"
            :key="task.id"
            class="mb-2"
            @click="selectedTask && selectedTask.id === task.id ? deselectTask() : selectTask(task)"
            :color="
              selectedTask && selectedTask.id === task.id ? 'blue-grey-lighten-3' : ''
            "
            :style="{ backgroundColor: task.tarea.color || '#6f6f6f', color: '#fff' }"
          >
            <v-card-title class="font-weight-bold">{{ task.nombre }}</v-card-title>
            <v-card-subtitle>
              {{ task.cantidad_completadas }} / {{ task.cantidad_para_completar }}
            </v-card-subtitle>
            <v-progress-linear
              :model-value="Number(task.progress)"
              color="blue lighten-1"
              height="10"
            ></v-progress-linear>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn icon @click.stop="showEditTaskDialog(task)">
                <v-icon>mdi-cog</v-icon>
              </v-btn>
            </v-card-actions>
            <v-icon
                v-if="selectedTask && selectedTask.id === task.id"
                color="white"
                style="position: absolute; top: 5px; right: 5px;"
              >
                mdi-check-circle
              </v-icon>
          </v-card>
        </div>
        <div v-show="tasks.length === 0">No hay tareas disponibles</div>
      </v-col>
    </v-row>

    <v-dialog v-model="manageSessionsDialog" max-width="700px" >
      <v-card>
        <v-card-title>Sesiones</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item v-for="session in sessions" :key="session.id">
              <v-list-item-title>{{ session.nombre }}</v-list-item-title>
              <template v-slot:append>
                <v-btn
                  icon
                  @click="
                    selectSession(session);
                    manageSessionsDialog = false;
                  "
                >
                  <v-icon>mdi-check-circle</v-icon>
                </v-btn>
                <v-btn icon @click="showEditSessionDialog(session)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="confirmDeleteSession(session)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="showAddSessionDialog">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="manageSessionsDialog = false"> Cerrar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="addSessionDialog" max-width="500px">
      <v-card>
        <v-card-title>Crear Sesión</v-card-title>
        <v-card-text>
          <v-text-field v-model="newSession.nombre" label="Nombre"></v-text-field>
          <v-text-field
            v-model.number="newSession.duracion_minutos"
            label="Duración en minutos"
            type="number"
          ></v-text-field>
          <v-checkbox v-model="newSession.obligatoria" label="Obligatoria"></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="addSession">Guardar</v-btn>
          <v-btn color="error" text @click="addSessionDialog = false"> Cancelar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="editSessionDialog" max-width="500px">
      <v-card>
        <v-card-title>Editar Sesión</v-card-title>
        <v-card-text>
          <v-text-field v-model="selectedSession.nombre" label="Nombre"></v-text-field>
          <v-text-field
            v-model.number="selectedSession.duracion_minutos"
            label="Duración en minutos"
            type="number"
          ></v-text-field>
          <v-checkbox
            v-model="selectedSession.obligatoria"
            label="Obligatoria"
          ></v-checkbox>
        </v-card-text>
        <v-color-picker v-model="selectedSession.color" label="Color de la sesión"></v-color-picker>
        <v-card-actions>
          <v-btn color="success" @click="updateSession">Guardar</v-btn>
          <v-btn color="error" text @click="editSessionDialog = false"> Cancelar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteSessionConfirmDialog" max-width="300px">
      <v-card>
        <v-card-title>Confirmar Eliminación</v-card-title>
        <v-card-text> ¿Estás seguro que deseas eliminar esta sesión? </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="deleteSession">Borrar</v-btn>
          <v-btn color="grey" text @click="deleteSessionConfirmDialog = false">
            Cancelar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="addTaskDialog" max-width="500px">
      <v-card>
        <v-card-title>Añadir Tarea</v-card-title>
        <v-card-text>
          <v-text-field v-model="newTask.nombre" label="Nombre de la tarea"></v-text-field>
          <v-textarea v-model="newTask.descripcion" label="Descripción de la tarea"></v-textarea>
          <v-text-field v-model="newTask.fecha_limite" label="Fecha límite" type="date"></v-text-field>
          <v-select
            v-model="newTask.actividadId"
            :items="actividades"
            item-text="nombre"
            item-value="id"
            label="Actividad asociada"
          ></v-select>
          <v-text-field v-model="newTask.cantidad_para_completar" label="Cantidad de sesiones a completar" type="number"></v-text-field>
          <v-color-picker v-model="newTask.color" label="Color de la tarea"></v-color-picker>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="addTask">Guardar</v-btn>
          <v-btn color="error" text @click="addTaskDialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="editTaskDialog" max-width="500px">
      <v-card>
        <v-card-title>Editar Tarea</v-card-title>
        <v-card-text>
          <v-text-field v-model="selectedTask.nombre" label="Nombre de la tarea"></v-text-field>
          <v-textarea v-model="selectedTask.descripcion" label="Descripción de la tarea"></v-textarea>
          <v-text-field v-model="selectedTask.fecha_limite" label="Fecha límite" type="date"></v-text-field>
          <v-select
            v-model="selectedTask.actividadId"
            :items="actividades"
            item-text="nombre"
            item-value="id"
            label="Actividad asociada"
          ></v-select>
          <v-text-field v-model="selectedTask.cantidad_completadas" label="Cantidad completadas" type="number"></v-text-field>
          <v-text-field v-model="selectedTask.cantidad_para_completar" label="Cantidad de sesiones que faltan" type="number"></v-text-field>
          <v-color-picker v-model="selectedTask.color" label="Color de la tarea"></v-color-picker>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="updateTask">Guardar</v-btn>
          <v-btn color="error" text @click="editTaskDialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


  </v-container>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { sendNotificationWithCustomConfig } from '@/utils/notificationHelper';

const timer = ref(60 * 60); // 60 minutes by default
const timerRunning = ref(false);
const interval = ref(null);
const sessions = ref([]);
const tasks = ref([]);
const manageSessionsDialog = ref(false);
const addSessionDialog = ref(false);
const editSessionDialog = ref(false);
const deleteSessionConfirmDialog = ref(false);
const selectedSession = ref({});
const sessionToDelete = ref(null);
const newSession = ref({
  nombre: "",
  duracion_minutos: 60,
  obligatoria: false,
});
const selectedTask = ref(null);
const addTaskDialog = ref(false);
const editTaskDialog = ref(false);
const newTask = ref({
  nombre: "",
  cantidad_para_completar: 1,
  cantidad_completadas: 0,
});
const showAlert = ref(false);

onMounted(() => {
  fetchSessions();
  fetchTasks();
  fetchActividades();
});

const formattedTime = computed(() => {
  const minutes = Math.floor(timer.value / 60);
  const seconds = timer.value % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
});

function startTimer() {
  if (!timerRunning.value) {
    timerRunning.value = true;
    interval.value = setInterval(() => {
      if (timer.value > 0) {
        timer.value--;
      } else {
        handleTimerEnd();
      }
    }, 1000);
  }
}

const actividades = ref([]);

async function fetchActividades() {
  try {
    const response = await fetch("http://localhost:8000/actividades/");
    if (response.ok) {
      const data = await response.json();
      actividades.value = data.results; // Asumiendo que la respuesta tiene un campo 'results'
    } else {
      console.error("Error al obtener actividades:", response.statusText);
    }
  } catch (error) {
    console.error("Error en fetchActividades:", error);
  }
}
function deseleccionarSesion() {
  selectedSession.value = {};
  resetTimer();
}
function pauseTimer() {
  timerRunning.value = false;
  clearInterval(interval.value);
}

function resetTimer() {
  timerRunning.value = false;
  clearInterval(interval.value);
  timer.value = selectedSession.value.duracion_minutos
    ? selectedSession.value.duracion_minutos * 60
    : 60 * 60;
}

async function handleTimerEnd() {
  clearInterval(interval.value);
  timerRunning.value = false;
  showAlert.value = true;
  sendNotificationWithCustomConfig({
      component: "WelcomeNotification",
      props: {
        title: '¡Tiempo cumplido! ⏲️',
        subtitle: 'Terminaste esta sesión 🎉.',
        icon: 'mdi mdi-check-circle-outline',
        color: "green",
        duration:1000000,

      },
    }, {
      position: 'top-center'
    });
  if (selectedTask.value) {
    selectedTask.value.cantidad_completadas++;
    await updateTask();
  }

  resetTimer();
}

async function fetchSessions() {
  try {
    const response = await fetch("http://localhost:8000/sesiones/");
    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data.results)) {
        sessions.value = data.results;
      } else {
        console.error("Error: La respuesta de /sesiones/ no es un array", data);
        sessions.value = [];
      }
    } else {
      console.error("Error al obtener las sesiones:", response.status);
      sessions.value = [];
    }
  } catch (error) {
    console.error("Error en fetchSessions:", error);
    sessions.value = [];
  }
}

async function fetchTasks() {
  try {
    const response = await fetch("http://localhost:8000/tareasTimer/");
    if (response.ok) {
      const data = await response.json();
      tasks.value = data.results.map(task => ({
        ...task,
        id: task.id,
        nombre: task.tarea.nombre, // Accediendo al nombre de la tarea
        descripcion: task.tarea.descripcion, // Descripción de la tarea
        actividad: task.tarea.actividad.nombre, // Nombre de la actividad asociada
        cantidad_completadas: task.cantidad_completadas,
        cantidad_para_completar: task.cantidad_para_completar,
        progress: task.progress
      }));
    } else {
      console.error("Error al obtener las tareas:", response.statusText);
      tasks.value = [];
    }
  } catch (error) {
    console.error("Error en fetchTasks:", error);
    tasks.value = [];
  }
}
function showAddSessionDialog() {
  newSession.value = { nombre: "", duracion_minutos: 60, obligatoria: false };
  addSessionDialog.value = true;
}

async function addSession() {
  const response = await fetch("http://localhost:8000/sesiones/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newSession.value),
  });

  if (response.ok) {
    addSessionDialog.value = false;
    fetchSessions();
    push.success({
      title: "Sesión creada correctamente",
    })
  } else {
    console.error("Error adding session");
    try {
      const errorData = await response.json();
      console.error("Detalles del error:", errorData);
    } catch (error) {
      console.error(
        "No se pudo obtener el cuerpo del error:",
        response.status,
        response.statusText
      );
    }
  }
}

function showEditSessionDialog(session) {
  selectedSession.value = { ...session };
  editSessionDialog.value = true;
}

async function updateSession() {
  const response = await fetch(
    `http://localhost:8000/sesiones/${selectedSession.value.id}/`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selectedSession.value),
    }
  );

  if (response.ok) {
    editSessionDialog.value = false;
    fetchSessions();
    push.success({
      title: "Editado con éxito!",
      message: 'Sesión editada correctamente.',
    })
  } else {
    console.error("Error updating session");
  }
}

function confirmDeleteSession(session) {
  sessionToDelete.value = session;
  deleteSessionConfirmDialog.value = true;
}

async function deleteSession() {
  const response = await fetch(
    `http://localhost:8000/sesiones/${sessionToDelete.value.id}/`,
    {
      method: "DELETE",
    }
  );

  if (response.ok) {
    deleteSessionConfirmDialog.value = false;
    fetchSessions();
    if (selectedSession.value && selectedSession.value.id === sessionToDelete.value.id) {
      selectedSession.value = {};
      resetTimer();
    }
  } else {
    console.error("Error deleting session");
  }
}

function selectSession(session) {
  selectedSession.value = session;
  timer.value = session.duracion_minutos * 60;
}

function selectTask(task) {
  selectedTask.value = task;
}
function deselectTask() {
  selectedTask.value = null;
}
function showAddTaskDialog() {
  newTask.value = { nombre: "", cantidad_para_completar: 1, cantidad_completadas: 0 };
  addTaskDialog.value = true;
}

async function addTask() {
  const response = await fetch("http://localhost:8000/tareasTimer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newTask.value),
  });

  if (response.ok) {
    addTaskDialog.value = false;
    fetchTasks();
    push.success({
      title: "Tarea creada correctamente",
    })
  } else {
    console.error("Error adding task");
  }
}

function showEditTaskDialog(task) {
  selectedTask.value = { ...task };
  editTaskDialog.value = true;
}

async function updateTask() {
  const response = await fetch(
    `http://localhost:8000/tareasTimer/${selectedTask.value.id}/`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selectedTask.value),
    }
  );

  if (response.ok) {
    editTaskDialog.value = false;
    push.success({
      title: "Cambio guardado!",
      message: 'Tarea editada correctamente.',
    })
    fetchTasks();
  } else {
    console.error("Error updating task");
  }
}
</script>
<style scoped>

.icono-deseleccionar {
  font-size: 18px; /* Ajusta el tamaño */
  cursor: pointer;  /* Cambia el cursor al pasar por encima */
}
.v-container {
  font-family: "Roboto", sans-serif; /* Fuente principal */
}

.v-card {
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Sombra suave */
}

.v-card-title.text-center {
  font-weight: 500;
  font-size: 24px;
  color: #2196f3; /* Azul primario */
  margin-bottom: 10px;
}

.v-card-text.text-center.display-1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.v-btn {
  margin: 0 5px;
  text-transform: none; /* Quita la transformación a mayúsculas por defecto */
}

.v-card-title {
  font-size: 20px;
  color: #2196f3; /* Azul primario */
}

.v-card.mb-2 {
  border: 1px solid #ccc; /* Borde ligero */
  transition: box-shadow 0.2s ease-in-out;
}

.v-card.mb-2:hover {
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada al hacer hover */
}

.v-card-title.font-weight-bold {
  font-size: 18px;
  color: #333;
}

.v-card-subtitle {
  font-size: 14px;
  color: #666;
}

.v-dialog {
  border-radius: 10px;
}

.v-dialog .v-card-title {
  font-size: 20px;
  color: #2196f3;
  padding-bottom: 0;
}

.v-dialog .v-card-text {
  padding-top: 10px;
}

.v-dialog .v-card-actions {
  padding-top: 0;
}

.v-dialog .v-text-field {
  margin-bottom: 10px;
}

.v-dialog .v-btn {
  margin-top: 10px;
}
.v-dialog .v-checkbox {
  margin-top: 5px;
}

</style>
