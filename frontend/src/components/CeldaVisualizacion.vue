<template>
  <v-card class="celda">
    <v-card-text>
      <div>ID: {{ celda.id }}</div>
      <div>Contenido: {{ celda.contenido }}</div>
      <div v-if="elementos && elementos.length > 0">
        Elementos de esta celda:
        <ul>
          <li v-for="elemento in elementos" :key="elemento.id">
            {{ elemento.descripcion }}
          </li>
        </ul>
      </div>
      <div v-else>No hay elementos relacionados con esta celda.</div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    celda: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      elementos: [],
    };
  },
  async mounted() {
    await this.fetchElementos();
  },
  methods: {
    async fetchElementos() {
      try {
        const response = await fetch(
          `http://localhost:8000/elementos/?celda_id=${this.celda.id}`
        );
        if (response.ok) {
          const data = await response.json();
          // Asegúrate de que 'data' es un array y tiene la propiedad 'results'
          if (Array.isArray(data.results)) {
            this.elementos = data.results.filter(
              (elemento) => elemento.celda === this.celda.id
            );
          } else if (Array.isArray(data)) {
            this.elementos = data.filter(
              (elemento) => elemento.celda === this.celda.id
            );
          } else {
            console.error("Los datos recibidos no son un array:", data);
            this.elementos = [];
          }
        } else {
          console.error(
            "Error al cargar los elementos:",
            response.statusText
          );
        }
      } catch (error) {
        console.error("Error al hacer fetch de los elementos:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Estilos para la celda, si los necesitas */
</style>