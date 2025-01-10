<template>
<div class="actividad-form">
    <h2>{{ actividadId ? 'Editar' : 'Crear' }} Actividad</h2>
    <form @submit.prevent="submitForm">
    <div>
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="actividad.nombre" required>
    </div>
    <div>
        <label for="descripcion">Descripción:</label>
        <textarea id="descripcion" v-model="actividad.descripcion"></textarea>
    </div>
    <div>
        <label for="fecha_inicio">Fecha de inicio:</label>
        <input type="date" id="fecha_inicio" v-model="actividad.fecha_inicio">
    </div>
    <div>
        <label for="fecha_fin">Fecha de fin:</label>
        <input type="date" id="fecha_fin" v-model="actividad.fecha_fin">
    </div>
    <div>
        <label for="color">Color:</label>
        <input type="color" id="color" v-model="actividad.color">
    </div>
    <button type="submit">Guardar</button>
    </form>
</div>
</template>

<script>
export default {
  props: {
    actividadId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      actividad: {
        nombre: '',
        descripcion: '',
        fecha_inicio: '',
        fecha_fin: '',
        color: '#0000FF'
      }
    };
  },
  mounted() {
    if (this.actividadId) {
      this.fetchActividad();
    }
  },
  methods: {
    async fetchActividad() {
      const response = await fetch(`http://localhost:8000/actividades/${this.actividadId}/`);
      if (response.ok) {
        this.actividad = await response.json();
      } else {
        console.error("Failed to load activity", response.statusText);
      }
    },
    async submitForm() {
      const method = this.actividadId ? 'PUT' : 'POST';
      const url = this.actividadId
        ? `http://localhost:8000/actividades/${this.actividadId}/`
        : 'http://localhost:8000/actividades/';
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.actividad)
      });
      if (response.ok) {
        alert('Actividad guardada con éxito');
        this.$emit('activity-saved');
      } else {
        console.error("Error saving activity", response.statusText);
      }
    }
  }
};
</script>
<style scoped>
.actividad-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.actividad-form h2 {
  text-align: center;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
input[type="color"],
textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

