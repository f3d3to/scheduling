<template>
  <div class="pomodoro-timer">
    <!-- Gestión de Sesiones -->
    <div class="session-management">
      <h2>Manage Sessions</h2>
      <form @submit.prevent="createSession">
        <input
          v-model="newSession.nombre"
          placeholder="Session Name"
          required
        />
        <input
          v-model.number="newSession.duracion_minutos"
          type="number"
          placeholder="Duration (minutes)"
          required
        />
        <label>
          <input
            type="checkbox"
            v-model="newSession.es_obligatoria"
          />
          Mandatory
        </label>
        <button type="submit">Create Session</button>
      </form>
    </div>

    <!-- Selector de Sesiones -->
    <div class="session-selector">
      <h2>Choose a Session</h2>
      <select v-model="selectedSession" @change="onSessionChange">
        <option v-for="session in sessions" :key="session.id" :value="session">
          {{ session.nombre }} ({{ session.duracion_minutos }} min)
        </option>
      </select>
    </div>

    <!-- Temporizador -->
    <div class="timer-display">
      <h1>{{ formattedTime }}</h1>
      <button
        @click="isRunning ? pauseTimer() : startTimer()"
        :class="{ start: !isRunning, pause: isRunning }"
      >
        {{ isRunning ? "Pause" : "Start" }}
      </button>
    </div>

    <p class="motivational-message">{{ motivationalMessage }}</p>

    <!-- Gestión de Tareas -->
    <div class="tasks-section">
      <h2>Tasks</h2>
      <ul class="task-list">
        <li v-for="task in tasks" :key="task.id">
          <span>{{ task.nombre }}</span>
          <span
            v-if="task.esta_realizada"
            class="completed"
          >
            (Completed)
          </span>
        </li>
      </ul>
      <button class="add-task" @click="addTask">+ Add Task</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRunning: false,
      timeRemaining: 0,
      timer: null,
      sessions: [],
      tasks: [],
      selectedSession: null,
      motivationalMessage: "Time to focus!",
      newSession: {
        nombre: "",
        duracion_minutos: 25,
        es_obligatoria: false,
      },
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeRemaining / 60);
      const seconds = this.timeRemaining % 60;
      return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    },
  },
  methods: {
    async fetchSessions() {
      try {
        const response = await fetch("http://localhost:8000/sesiones/");
        if (!response.ok) {
          throw new Error("Failed to fetch sessions");
        }
        this.sessions = await response.json();
      } catch (error) {
        console.error(error);
      }
    },
    async fetchTasks() {
      try {
        const response = await fetch("http://localhost:8000/tareas/");
        if (!response.ok) {
          throw new Error("Failed to fetch tasks");
        }
        this.tasks = await response.json();
      } catch (error) {
        console.error(error);
      }
    },
    async createSession() {
      try {
        const response = await fetch("http://localhost:8000/sesiones/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.newSession),
        });
        if (!response.ok) {
          throw new Error("Failed to create session");
        }
        const newSession = await response.json();
        this.sessions = [...this.sessions, newSession]; // Actualización Reactiva
        this.newSession = {
          nombre: "",
          duracion_minutos: 25,
          es_obligatoria: false,
        };
      } catch (error) {
        console.error(error);
      }
    },
    async addTask() {
      const taskName = prompt("Enter task name:");
      if (taskName) {
        try {
          const response = await fetch("http://localhost:8000/tareas/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              nombre: taskName,
              cantidad_para_completar: 1,
              usuario: 1, // Cambiar por el ID del usuario autenticado
            }),
          });
          if (!response.ok) {
            throw new Error("Failed to add task");
          }
          const newTask = await response.json();
          this.tasks = [...this.tasks, newTask]; // Actualización Reactiva
        } catch (error) {
          console.error(error);
        }
      }
    },
    onSessionChange() {
      if (this.selectedSession) {
        this.timeRemaining = this.selectedSession.duracion_minutos * 60;
        this.motivationalMessage = `Session: ${this.selectedSession.nombre}`;
      }
    },
    startTimer() {
      if (!this.isRunning) {
        this.isRunning = true;
        this.timer = setInterval(() => {
          if (this.timeRemaining > 0) {
            this.timeRemaining--;
          } else {
            this.pauseTimer();
            alert("Time's up!");
          }
        }, 1000);
      }
    },
    pauseTimer() {
      this.isRunning = false;
      clearInterval(this.timer);
    },
    resetTimer() {
      this.pauseTimer();
      if (this.selectedSession) {
        this.timeRemaining = this.selectedSession.duracion_minutos * 60;
      }
    },
  },
  mounted() {
    this.fetchSessions();
    this.fetchTasks();
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
/* Estilos mejorados */
.pomodoro-timer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #242424;
  color: white;
  padding: 20px;
}

.session-management form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.session-management input,
.session-management button {
  padding: 10px;
  font-size: 1rem;
}

.session-selector {
  margin-bottom: 20px;
  text-align: center;
}

.timer-display h1 {
  font-size: 4rem;
  margin: 20px 0;
}

.timer-display button {
  padding: 10px 30px;
  font-size: 1.5rem;
  cursor: pointer;
}

.motivational-message {
  margin-top: 20px;
  font-size: 1.2rem;
  text-align: center;
}

.tasks-section {
  margin-top: 30px;
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.tasks-section h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 10px 0;
}

.task-list li {
  background: #333;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  color: white;
}

.add-task {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  background: #444;
  color: white;
  border: 1px solid white;
  border-radius: 5px;
}
</style>
