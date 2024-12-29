<template>
  <GridLayout
    v-if="layoutGenerado"
    :layout="layout"
    :col-num="columnas"
    :is-draggable="true"
    :is-resizable="false"
    :responsive="false"
    :margin="[0, 0]"
    :auto-size="true"
  >
    <GridItem
      v-for="item in layout"
      :key="item.i"
      :x="item.x"
      :y="item.y"
      :w="item.w"
      :h="item.h"
      :i="item.i"
    >
      <CeldaVisualizacion :celda="getCeldaById(item.i)" />
    </GridItem>
  </GridLayout>
</template>

<script>
import { defineComponent, watch } from "vue";
import { GridLayout, GridItem } from "vue3-grid-layout-next";
import CeldaVisualizacion from "./CeldaVisualizacion.vue";

export default defineComponent({
  components: {
    GridLayout,
    GridItem,
    CeldaVisualizacion,
  },
  data() {
    return {
      layout: [],
      celdas: [],
      columnas: 7, // Valor inicial
      layoutGenerado: false, // Controla la renderización de GridLayout
      draggable: true,
      resizable: true,
      index: 0,
      eventLog: [],
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const planificadorId = this.$route.params.id || "pk";
        const response = await fetch(
          `http://localhost:8000/estructuras-planificador/${planificadorId}/`
        );
        if (response.ok) {
          const data = await response.json();
          this.columnas = data.columnas;
          this.celdas = Object.entries(data.tabla).map(([coordenadas, celda]) => ({
            ...celda,
            coordenadas,
          }));
          this.layout = this.generateLayout(this.celdas);
          this.layoutGenerado = true; // Indicar que el layout está listo
        } else {
          console.error("Error al cargar los datos:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de los datos:", error);
      }
    },
    generateLayout(celdas) {
      return celdas.map((celda) => {
        const [fila, columna] = celda.coordenadas.split(",").map(Number);
        return {
          i: String(celda.id),
          x: columna - 1,
          y: fila - 1,
          w: 1,
          h: 1,
        };
      });
    },
    getCeldaById(id) {
      return this.celdas.find((celda) => celda.id === parseInt(id));
    },
  },
});
</script>


<style scoped>
.vue-grid-layout {
  background-color: #f5f5f5; /* Un gris claro de fondo */
  border-radius: 10px; /* Bordes redondeados */
  padding: 10px; /* Espacio interno */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Sombra suave */
  width: 100%;
}
.grid-item {
  width: 100%;
  overflow: hidden; /* Asegura que el contenido respete los bordes redondeados */
}
.grid::before {
    content: '';
    background-size: calc(calc(100% - 5px) / 12) 40px;
    background-image: linear-gradient(
            to right,
            lightgrey 1px,
            transparent 1px
    ),
    linear-gradient(to bottom, lightgrey 1px, transparent 1px);
    height: calc(100% - 5px);
    width: calc(100% - 5px);
    position: absolute;
    background-repeat: repeat;
    margin:5px;
}

</style>