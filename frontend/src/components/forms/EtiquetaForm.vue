<template>
    <div class="etiqueta-form">
      <h2>{{ etiquetaId ? 'Editar' : 'Crear' }} Etiqueta</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="nombre">Nombre:</label>
          <input type="text" id="nombre" v-model="etiqueta.nombre" required>
        </div>
        <div>
          <label for="descripcion">Descripción:</label>
          <textarea id="descripcion" v-model="etiqueta.descripcion"></textarea>
        </div>
        <div>
          <label for="color">Color:</label>
          <input type="color" id="color" v-model="etiqueta.color">
        </div>
        <button type="submit">Guardar</button>
      </form>
    </div>
</template>
<script>
export default {
  props: {
    etiquetaId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      etiqueta: {
        nombre: '',
        descripcion: '',
        color: '#FFFFFF'
      }
    };
  },
  mounted() {
    if (this.etiquetaId) {
      this.fetchEtiqueta();
    }
  },
  methods: {
    async fetchEtiqueta() {
      const response = await fetch(`http://localhost:8000/etiquetas/${this.etiquetaId}/`);
      if (response.ok) {
        this.etiqueta = await response.json();
      } else {
        console.error("Failed to load label", response.statusText);
      }
    },
    async submitForm() {
      const method = this.etiquetaId ? 'PUT' : 'POST';
      const url = this.etiquetaId
        ? `http://localhost:8000/etiquetas/${this.etiquetaId}/`
        : 'http://localhost:8000/etiquetas/';
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.etiqueta)
      });
      if (response.ok) {
        alert('Etiqueta guardada con éxito');
        this.$emit('label-saved');
      } else {
        console.error("Error saving label", response.statusText);
      }
    }
  }
};
</script>
<style scoped>
.etiqueta-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.etiqueta-form h2 {
  text-align: center;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
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

