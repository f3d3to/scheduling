
<template>
<div class="tarea-form">
    <h2>{{ tareaId ? 'Editar' : 'Crear' }} Tarea</h2>
    <form @submit.prevent="submitForm">
    <div>
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="tarea.nombre" required>
    </div>
    <div>
        <label for="descripcion">Descripción:</label>
        <textarea id="descripcion" v-model="tarea.descripcion"></textarea>
    </div>
    <div>
        <label for="fecha_limite">Fecha límite:</label>
        <input type="date" id="fecha_limite" v-model="tarea.fecha_limite">
    </div>
    <div>
        <label for="color">Color:</label>
        <input type="color" id="color" v-model="tarea.color">
    </div>
    <div>
        <label for="esta_realizada">Completada:</label>
        <input type="checkbox" id="esta_realizada" v-model="tarea.esta_realizada">
    </div>
    <button type="submit">Guardar</button>
    </form>
</div>
</template>
<script>
export default {
  props: {
    tareaId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      tarea: {
        nombre: '',
        descripcion: '',
        fecha_limite: '',
        color: '#FF0000',
        esta_realizada: false
      }
    };
  },
  mounted() {
    if (this.tareaId) {
      this.fetchTarea();
    }
  },
  methods: {
    async fetchTarea() {
      const response = await fetch(`http://localhost:8000/tareas/${this.tareaId}/`);
      if (response.ok) {
        this.tarea = await response.json();
      } else {
        console.error("Failed to load task", response.statusText);
      }
    },
    async submitForm() {
      const method = this.tareaId ? 'PUT' : 'POST';
      const url = this.tareaId
        ? `http://localhost:8000/tareas/${this.tareaId}/`
        : 'http://localhost:8000/tareas/';
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.tarea)
      });
      if (response.ok) {
        alert('Tarea guardada con éxito');
        this.$emit('task-saved');
      } else {
        console.error("Error saving task", response.statusText);
      }
    }
  }
};
</script>

<style scoped>
.tarea-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.tarea-form h2 {
  text-align: center;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
input[type="color"],
textarea,
input[type="checkbox"] {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #FF0000;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #cc0000;
}
</style>

