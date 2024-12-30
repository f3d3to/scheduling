<template>
  <v-card class="celda-visualizacion">
    <div v-if="elementos && elementos.length > 0" class="celda-elementos">
      <div
        v-for="elemento in elementos"
        :key="elemento.id"
        class="elemento-contenedor"
      >
        <ElementoVisualizacion :elemento="elemento" />
      </div>
    </div>
    <div v-else class="celda-sin-elementos">
      No hay elementos relacionados con esta celda.
    </div>
  </v-card>
</template>

<script>
import ElementoVisualizacion from "@planificadorDetalle/ElementoVisualizacion.vue";

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
  components: {
    ElementoVisualizacion,
  },
  methods: {
    async fetchElementos() {
      try {
        const response = await fetch(`http://localhost:8000/elementos/`);
        if (response.ok) {
          const data = await response.json();
          const resultados = Array.isArray(data.results) ? data.results : data;
          this.elementos = resultados.filter(
            (elemento) => elemento.celda === this.celda.id
          );
        } else {
          console.error("Error al cargar los elementos:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de los elementos:", error);
      }
    },
  },
  async mounted() {
    await this.fetchElementos();
  },
};
</script>

<style scoped>
.celda-visualizacion {
  background-color: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  height: 100%;
  overflow: auto;
}

.elemento-contenedor {
  margin-bottom: 10px;
}
.celda-sin-elementos {
  margin-bottom: 10px;
}
</style>