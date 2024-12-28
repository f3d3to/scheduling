<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>{{ planificador.nombre }}</h1>
      </v-col>
    </v-row>
    <v-row class="fila-planificador">
      <div v-if="celdasArray.length > 0" class="drag-area">
        <draggable
          v-model="celdasArray"
          :group="'celdas'"
          item-key="id"
          @end="onDragEnd"
        >
          <template v-slot:item="{ element }">
            <CeldaVisualizacion
              :celda="element"
              :ancho-columna="planificador.ancho_columna"
              @celda-seleccionada="celdaSeleccionada = $event"
              @actualizar-celda="actualizarCelda"
            />
          </template>
          <template v-slot:header></template>
          <template v-slot:footer></template>
        </draggable>
      </div>
      <div v-else>
        No hay elementos para mostrar.
      </div>
    </v-row>
  </v-container>
</template>

<script>
import CeldaVisualizacion from "./CeldaVisualizacion.vue";
import draggable from "vuedraggable";
export default {
  components: {
    CeldaVisualizacion,
    draggable,
  },
  data() {
    return {
      planificador: {
        nombre: "",
        ancho_columna: 0,
        configuracion: {
          filas: 0,
          columnas: 0,
        },
      },
      celdasArray: [],
      celdaSeleccionada: null,
    };
  },
  computed: {},
  async created() {
    this.$slots; // Workaround para el warning de $scopedSlots
    const planificadorId = this.$route.params.id || 1;
    await this.cargarPlanificador(planificadorId);
  },
  methods: {
    async cargarPlanificador(planificadorId) {
      try {
        const response = await fetch(
          `http://localhost:8000/estructuras-planificador/${planificadorId}/`
        );
        if (response.ok) {
          const data = await response.json();
          this.planificador.nombre = data.nombre;
          this.planificador.ancho_columna = data.ancho_columna;
          this.planificador.configuracion = data.configuracion;

          // Asegurarse de que celdasArray sea siempre un array
          if (Array.isArray(data.tabla)) {
            this.celdasArray = data.tabla.map((celda, index) => ({
              ...celda,
              id: celda.id,
              coordinates: celda.coordinates,
            }));
          } else if (typeof data.tabla === "object" && data.tabla !== null) {
            this.celdasArray = Object.entries(data.tabla).map(
              ([coordinates, celda], index) => ({
                ...celda,
                id: celda.id,
                coordinates: coordinates,
              })
            );
          } else {
            this.celdasArray = [];
            console.warn("La respuesta del servidor no contiene un array o un objeto válido para 'tabla'.");
          }
        } else {
          console.error("Error al cargar el planificador:", response.status);
        }
      } catch (error) {
        console.error("Error al cargar el planificador:", error);
      }
    },
    async actualizarCelda(celdaActualizada) {
      try {
        const response = await fetch(
          `http://localhost:8000/celdas/${celdaActualizada.id}/`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              contenido: celdaActualizada.contenido,
            }),
          }
        );
        if (response.ok) {
          const index = this.celdasArray.findIndex(
            (celda) => celda.id === celdaActualizada.id
          );
          if (index !== -1) {
            this.celdasArray[index] = {
              ...this.celdasArray[index],
              contenido: celdaActualizada.contenido,
            };
          }
          this.celdaSeleccionada = null;
        } else {
          console.error("Error al actualizar la celda:", response.status);
        }
      } catch (error) {
        console.error("Error al actualizar la celda:", error);
      }
    },
    onDragEnd(evt) {
      console.log("Drag ended:", evt);
      // Aquí deberías implementar la lógica para actualizar el orden en el backend
      // después de que el usuario haya terminado de arrastrar y soltar los elementos.
      // Esto podría implicar enviar una petición al servidor con el nuevo orden de celdasArray.
    },
  },
};
</script>

<style scoped>
.fila-planificador {
  margin-top: 20px; /* Reduce el espacio entre la barra superior y la tabla */
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.drag-area {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>