<template>
  <div class="pomodoro-timer">
    <!-- Título -->
    <header class="header">
      <h1>Pomodoro Timer</h1>
    </header>

    <!-- Crear Sesiones -->
    <div class="session-management">
      <h2>Create a New Session</h2>
      <form @submit.prevent="createSession" class="session-form">
        <input
          v-model="newSession.nombre"
          type="text"
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
        <button type="submit">Add Session</button>
      </form>
    </div>

    <!-- Seleccionar Sesiones -->
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

    <!-- Mensaje Motivacional -->
    <p class="motivational-message">{{ motivationalMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRunning: false,
      timeRemaining: 0,
      timer: null,
      sessions: [], // Sesiones cargadas desde el backend
      selectedSession: null, // Sesión seleccionada por el usuario
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
        if (!response.ok) throw new Error("Failed to fetch sessions");
        this.sessions = await response.json();
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
        if (!response.ok) throw new Error("Failed to create session");

        const newSession = await response.json();
        this.sessions = [...this.sessions, newSession]; // Actualiza sesiones reactivamente
        this.newSession = {
          nombre: "",
          duracion_minutos: 25,
          es_obligatoria: false,
        };
      } catch (error) {
        console.error(error);
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
  background-color: #242424;
  color: white;
  padding: 20px;
}

.header h1 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.session-management {
  margin-bottom: 20px;
  width: 100%;
  max-width: 400px;
}

.session-management h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.session-management .session-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
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
</style>
