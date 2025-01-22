<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card :style="{ backgroundColor: pomodoroStore.selectedSession.color || '#dbd9d9', color: '#fff' }">
          <v-card-title class="text-center">Pomodoro </v-card-title>
          <v-card-title class="text-center" v-if="pomodoroStore.selectedSession">
            <strong>{{ pomodoroStore.selectedSession.nombre }}</strong>
            <v-icon
              v-if="pomodoroStore.selectedSession.id"
              class="icono-deseleccionar"
              size="25px"
              @click="pomodoroStore.deselectSession"
              title="Desmarcar sesión"
            >
              mdi-close
            </v-icon>
          </v-card-title>
          <v-card-text class="text-center display-1 font-weight-bold">
            {{ pomodoroStore.formattedTime }}
          </v-card-text>

          <v-card-text class="text-center" v-if="pomodoroStore.selectedTask">
            <strong>{{ pomodoroStore.selectedTask.nombre }}</strong>
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="pomodoroStore.startTimer" :disabled="pomodoroStore.timerRunning" prepend-icon="mdi-play">
              Iniciar
            </v-btn>
            <v-btn color="warning" @click="pomodoroStore.pauseTimer" :disabled="!pomodoroStore.timerRunning" prepend-icon="mdi-pause">
              Pausa
            </v-btn>
            <v-btn color="error" @click="pomodoroStore.resetTimer" prepend-icon="mdi-stop">Reiniciar</v-btn>
          </v-card-actions>

          <v-card-actions class="justify-center">
            <v-btn color="secondary" @click="manageSessionsDialog = true">
              <v-icon size="25px">mdi-dots-horizontal</v-icon>
              Sesiones
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="8">
        <v-card-title v-if="pomodoroStore.tasks.length > 0">
          Tareas
          <v-btn color="primary" @click="showAddTaskDialog" class="mb-2" v-if="pomodoroStore.tasks.length > 0">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-card-title>
        <div v-show="pomodoroStore.tasks.length > 0">
          <v-card
            v-for="task in pomodoroStore.tasks"
            :key="task.id"
            class="mb-2"
            @click="pomodoroStore.selectedTask && pomodoroStore.selectedTask.id === task.id ? pomodoroStore.deselectTask() : pomodoroStore.selectTask(task)"
            :color="pomodoroStore.selectedTask && pomodoroStore.selectedTask.id === task.id ? 'blue-grey-lighten-3' : ''"
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
              v-if="pomodoroStore.selectedTask && pomodoroStore.selectedTask.id === task.id"
              color="white"
              style="position: absolute; top: 5px; right: 5px;"
            >
              mdi-check-circle
            </v-icon>
          </v-card>
        </div>
        <div v-show="pomodoroStore.tasks.length === 0">No hay tareas disponibles</div>
      </v-col>
    </v-row>

    <v-dialog v-model="manageSessionsDialog" max-width="700px">
      <v-card>
        <v-card-title>Sesiones</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item v-for="session in pomodoroStore.sessions" :key="session.id">
              <v-list-item-title>{{ session.nombre }}</v-list-item-title>
              <template v-slot:append>
                <v-btn
                  icon
                  @click="
                    pomodoroStore.selectSession(session);
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
          <v-text-field v-model="pomodoroStore.selectedSession.nombre" label="Nombre"></v-text-field>
          <v-text-field
            v-model.number="pomodoroStore.selectedSession.duracion_minutos"
            label="Duración en minutos"
            type="number"
          ></v-text-field>
          <v-checkbox
            v-model="pomodoroStore.selectedSession.obligatoria"
            label="Obligatoria"
          ></v-checkbox>
        </v-card-text>
        <v-color-picker v-model="pomodoroStore.selectedSession.color" label="Color de la sesión"></v-color-picker>
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
            :items="pomodoroStore.actividades"
            item-title="nombre"
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
          <v-text-field v-model="pomodoroStore.selectedTask.nombre" label="Nombre de la tarea"></v-text-field>
          <v-textarea v-model="pomodoroStore.selectedTask.descripcion" label="Descripción de la tarea"></v-textarea>
          <v-text-field v-model="pomodoroStore.selectedTask.fecha_limite" label="Fecha límite" type="date"></v-text-field>
          <v-select
            v-model="newTask.actividadId"
            :items="pomodoroStore.actividades"
            item-title="nombre"
            item-value="id"
            label="Actividad asociada"
          ></v-select>
          <v-text-field v-model="pomodoroStore.selectedTask.cantidad_completadas" label="Cantidad completadas" type="number"></v-text-field>
          <v-text-field v-model="pomodoroStore.selectedTask.cantidad_para_completar" label="Cantidad de sesiones que faltan" type="number"></v-text-field>
          <v-color-picker v-model="pomodoroStore.selectedTask.color" label="Color de la tarea"></v-color-picker>
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
import { usePomodoroStore } from "@/store/PomodoroStore";

const pomodoroStore = usePomodoroStore();

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
  actividadId: null,
  cantidad_para_completar: 1,
  cantidad_completadas: 0,
});
const showAlert = ref(false);

onMounted(() => {
  pomodoroStore.fetchSessions();
  pomodoroStore.fetchTasks();
  pomodoroStore.fetchActividades();
});

const formattedTime = computed(() => {
  const minutes = Math.floor(timer.value / 60);
  const seconds = timer.value % 60;
  return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
});

function startTimer() {
  if (!pomodoroStore.timerRunning) {
    pomodoroStore.startTimer();
  }
}

function deseleccionarSesion() {
  pomodoroStore.deselectSession();
}

function pauseTimer() {
  pomodoroStore.pauseTimer();
}

function resetTimer() {
  pomodoroStore.resetTimer();
}

async function handleTimerEnd() {
  pomodoroStore.handleTimerEnd();
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
}

function showAddSessionDialog() {
  newSession.value = { nombre: "", duracion_minutos: 60, obligatoria: false };
  addSessionDialog.value = true;
}

async function addSession() {
  await pomodoroStore.createSession(newSession.value);
  addSessionDialog.value = false;
  push.success({
      title: "Sesión creada correctamente",
  })
}

function showEditSessionDialog(session) {
  pomodoroStore.selectedSession = { ...session };
  editSessionDialog.value = true;
}

async function updateSession() {
  await pomodoroStore.updateSession(pomodoroStore.selectedSession);
  editSessionDialog.value = false;
  push.success({
      title: "Editado con éxito!",
      message: 'Sesión editada correctamente.',
      position: 'top-right'

  })

}
function confirmDeleteSession(session) {
  sessionToDelete.value = session;
  deleteSessionConfirmDialog.value = true;
}

async function deleteSession() {
  await pomodoroStore.deleteSession(sessionToDelete.value.id);
  deleteSessionConfirmDialog.value = false;
}

function selectSession(session) {
  pomodoroStore.selectSession(session);
  timer.value = session.duracion_minutos * 60;
}

function selectTask(task) {
  pomodoroStore.selectedTask = task;
}

function deselectTask() {
  pomodoroStore.selectedTask = null;
}

function showAddTaskDialog() {
  newTask.value = {
    nombre: "",
    cantidad_para_completar: 1,
    cantidad_completadas: 0,
  };
  addTaskDialog.value = true;
}

async function addTask() {
  console.log("newTask: ", newTask.value)
  console.log("actividadId seleccionada:", newTask.actividadId);
  await pomodoroStore.createTask(newTask.value);
  addTaskDialog.value = false;
  push.success({
      title: "Tarea creada correctamente",
  })
}

function showEditTaskDialog(task) {
  pomodoroStore.selectedTask = { ...task };
  editTaskDialog.value = true;
}

async function updateTask() {
  try {
    await pomodoroStore.updateTask(pomodoroStore.selectedTask);

    await pomodoroStore.fetchTasks();

    editTaskDialog.value = false;
    push.success({
      title: "Cambio guardado!",
      message: 'Tarea editada correctamente.',
      position: 'top-right'
    });
  } catch (error) {
    console.error("Error actualizando tarea:", error);
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
