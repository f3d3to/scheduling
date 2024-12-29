<template>
  <v-card class="celda-visualizacion">
    <v-card-text>
      <h4 class="celda-titulo">ID: {{ celda.id }}</h4>
      <p class="celda-coordenadas">
        <strong>Contenido:</strong> Celda {{ celda.coordenadas }}
      </p>
      <div v-if="elementos && elementos.length > 0" class="celda-elementos">
        <strong>Elementos de esta celda:</strong>
        <ul>
          <li v-for="elemento in elementos" :key="elemento.id">
            {{ elemento.descripcion }}
          </li>
        </ul>
      </div>
      <div v-else class="celda-sin-elementos">
        No hay elementos relacionados con esta celda.
      </div>
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
.celda-visualizacion {
  background-color: #fff; /* Fondo blanco */
  border: 1px solid #ddd; /* Borde gris claro */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra suave */
  transition: transform 0.2s ease, box-shadow 0.2s ease; /* Transición suave */
  height: 100%;
  overflow: auto;
  margin: 10px 0px;
}

.celda-visualizacion:hover {
  transform: translateY(-2px); /* Elevar ligeramente al pasar el mouse */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* Sombra más pronunciada al hover */
}

.celda-titulo {
  color: #333; /* Título más oscuro */
  margin-bottom: 5px; /* Espacio debajo del título */
}

.celda-coordenadas {
  margin-bottom: 10px; /* Espacio debajo de las coordenadas */
}

.celda-elementos ul {
  list-style: none; /* Sin viñetas */
  padding: 0;
  margin-bottom: 10px; /* Espacio debajo de la lista */
}

.celda-elementos li {
  background-color: #f8f8f8; /* Fondo gris claro para los ítems */
  border-left: 4px solid #4caf50; /* Borde izquierdo verde */
  padding: 5px 10px;
  margin-bottom: 5px;
  border-radius: 4px; /* Bordes redondeados */
}

.celda-sin-elementos {
  margin-bottom: 10px; /* Espacio debajo del mensaje */
}
</style>