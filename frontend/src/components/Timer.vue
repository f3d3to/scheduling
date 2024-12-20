<template>
  <div class="pomodoro-timer">
    <h1>Pomodoro Timer</h1>
    <div class="task-selector">
      <label for="task">Select Task:</label>
      <select id="task" v-model="selectedTask" @change="onTaskChange">
        <option v-for="task in tasks" :key="task.id" :value="task.id">
          {{ task.nombre }}
        </option>
      </select>
    </div>
    <div class="session-info">
      <p>Session: {{ currentSession ? currentSession.nombre : 'None selected' }}</p>
      <p>Duration: {{ currentSession ? currentSession.duracion_minutos : 0 }} minutes</p>
    </div>
    <div class="timer">
      <span>{{ formattedTime }}</span>
    </div>
    <div class="controls">
      <button @click="startTimer" :disabled="isRunning">Start</button>
      <button @click="pauseTimer" :disabled="!isRunning">Pause</button>
      <button @click="resetTimer">Reset</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "PomodoroTimer",
  data() {
    return {
      isRunning: false,
      timeRemaining: 25 * 60,
      timer: null,
      tasks: [],
      sessions: [],
      selectedTask: null,
      currentSession: null,
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
    async fetchTasks() {
      try {
        const response = await fetch("/api/tareas/");
        if (!response.ok) {
          throw new Error("Failed to fetch tasks");
        }
        this.tasks = await response.json();
      } catch (error) {
        console.error(error);
      }
    },
    async fetchSessions() {
      try {
        const response = await fetch("/api/sesiones/");
        if (!response.ok) {
          throw new Error("Failed to fetch sessions");
        }
        this.sessions = await response.json();
      } catch (error) {
        console.error(error);
      }
    },
    onTaskChange() {
      const selected = this.tasks.find((task) => task.id === this.selectedTask);
      if (selected) {
        this.currentSession = this.sessions.find(
          (session) => session.id === selected.sesion_id
        );
        this.timeRemaining = this.currentSession.duracion_minutos * 60;
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
      this.timeRemaining = this.currentSession
        ? this.currentSession.duracion_minutos * 60
        : 25 * 60;
    },
  },
  mounted() {
    this.fetchTasks();
    this.fetchSessions();
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.pomodoro-timer {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%; /* Asegura que ocupa todo el ancho */
  height: 100%; /* Asegura que ocupa todo el alto */
  background-color: #242424;
  color: white;
}

.timer {
  font-size: 6rem; /* Ajusta el tamaño del texto del temporizador */
  margin: 20px 0;
}

.controls button {
  margin: 10px;
  padding: 15px 30px;
  font-size: 1.5rem; /* Botones más grandes */
  cursor: pointer;
}

.task-selector {
  margin-bottom: 20px;
  text-align: center;
}
.task-selector label {
  font-size: 1.2rem;
  margin-right: 10px;
}
.task-selector select {
  font-size: 1.1rem;
  padding: 5px 10px;
}
.session-info {
  margin-bottom: 20px;
  text-align: center;
}
</style>
