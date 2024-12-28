<template>
  <div class="dragArea list-group w-full">
    <draggable
      :list="list"
      item-key="id"
      @change="log"
      @start="drag = true"
      @end="drag = false"
      class="flex flex-wrap"
    >
      <div
        v-for="element in list"
        :key="element.id"
        class="list-group-item m-1 rounded-md text-center"
        :style="{ width: anchoColumna + 'px' }"
      >
        <CeldaVisualizacion :celda="element" />
      </div>
    </draggable>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { VueDraggableNext as draggable } from "vue-draggable-next";
import CeldaVisualizacion from "./CeldaVisualizacion.vue";

export default defineComponent({
  components: {
    draggable,
    CeldaVisualizacion,
  },
  data() {
    return {
      list: [],
      drag: false,
      anchoColumna: 0,
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // Obtener el ID del planificador de la ruta o usar 'pk' por defecto
        const planificadorId = this.$route.params.id || 'pk';

        const response = await fetch(
          `http://localhost:8000/estructuras-planificador/${planificadorId}/`
        );
        if (response.ok) {
          const data = await response.json();
          this.anchoColumna = data.ancho_columna;
          this.list = Object.entries(data.tabla).map(
            ([coordenadas, celda]) => ({
              id: celda.id,
              contenido: celda.contenido,
              coordenadas,
            })
          );
          console.log(this.list);
        } else {
          console.error("Error al cargar los datos:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de los datos:", error);
      }
    },
    log(event) {
      console.log("Dragged element:", event);
      this.actualizarOrdenEnBackend();
    },
    async actualizarOrdenEnBackend() {
      // Lógica para actualizar el orden en el backend
    },
  },
});
</script>

<style>
.dragArea .list-group-item {
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dragArea .list-group-item:hover {
  background-color: lightcoral;
}
</style>