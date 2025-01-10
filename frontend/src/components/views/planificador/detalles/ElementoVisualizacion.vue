<template>
  <div class="elemento-visualizacion" @click="openDialog">
    <div class="visualizacion-container">
      <component
        :is="getComponent(elemento.content_type)"
        :elemento="elemento"
        :edit-mode="editMode"
        @save="handleSave"
      />
    </div>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline"> {{ elemento.nombre }}</span>
        </v-card-title>

        <v-card-text>
          <component
            :is="getComponent(elemento.content_type)"
            :elemento="elemento"
            :edit-mode="true"
            @save="handleSave"
          />
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialog">Cancelar</v-btn>
          <v-btn color="error" text @click="eliminarElemento">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import TareaVisualizacion from "@planificadorDetalle/TareaVisualizacion.vue";
import ActividadVisualizacion from "@planificadorDetalle/ActividadVisualizacion.vue";
import EtiquetaVisualizacion from "@planificadorDetalle/EtiquetaVisualizacion.vue";
import ComentarioVisualizacion from "@planificadorDetalle/EtiquetaVisualizacion.vue";
import EventoVisualizacion from "@planificadorDetalle/EventoVisualizacion.vue";
import ObjetivoVisualizacion from "@planificadorDetalle/ObjetivoVisualizacion.vue";
import RecurrenteVisualizacion from "@planificadorDetalle/RecurrenteVisualizacion.vue";
import EventoAsociadoVisualizacion from "@planificadorDetalle/EventoAsociadoVisualizacion.vue";

export default {
  props: {
    elemento: {
      type: Object,
      required: true,
    },
  },
  components: {
    TareaVisualizacion,
    ActividadVisualizacion,
    EtiquetaVisualizacion,
    ComentarioVisualizacion,
    EventoVisualizacion,
    ObjetivoVisualizacion,
    RecurrenteVisualizacion,
    EventoAsociadoVisualizacion,
  },
  data() {
    return {
      dialog: false,
      editMode: false,
    };
  },
  methods: {
    getComponent(contentType) {
      const mapping = {
        8: ActividadVisualizacion, // 'actividad'
        23: TareaVisualizacion, // 'tarea'
        15: EtiquetaVisualizacion, // 'etiqueta'
        10: ComentarioVisualizacion, // 'comentario'
        16: EventoVisualizacion, // 'evento'
        19: ObjetivoVisualizacion, // 'objetivo'
        21: RecurrenteVisualizacion, // 'recurrente'
        17: EventoAsociadoVisualizacion, // 'eventoasociado'
};
      return mapping[contentType] || "div";
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    async eliminarElemento() {
      try {
        const response = await fetch(`http://localhost:8000/elementos/${this.elemento.id}/`, {
          method: "DELETE",
        });

        if (response.ok) {
          this.$emit("elemento-eliminado", this.elemento.id);
          this.closeDialog();
        } else {
          console.error("Error al eliminar el elemento:", response.statusText);
        }
      } catch (error) {
        console.error("Error al eliminar el elemento:", error);
      }
    },
    handleSave(elementoActualizado) {
      this.$emit("elemento-actualizado", elementoActualizado);
      this.closeDialog();
    },
  },
};
</script>

<style scoped>
.elemento-visualizacion {
  cursor: pointer; /* Cambia el cursor a una mano para indicar que es clickable */
}

.visualizacion-container {
  flex-grow: 1;
}
</style>