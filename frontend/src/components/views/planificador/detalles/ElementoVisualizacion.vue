<template>
  <div class="elemento-visualizacion" @click="openDialog">
    <div class="visualizacion-container">
      <span class="elemento-nombre">{{ elemento.nombre }}</span>
    </div>

    <v-dialog v-model="dialog" max-width="800px">
      <component
        :is="getComponent(elemento.content_type)"
        :elemento="elemento"
        :edit-mode="true"
      />
    </v-dialog>
  </div>
</template>

<script>
import TareaVisualizacion from "@planificadorDetalle/TareaVisualizacion.vue";
import ActividadVisualizacion from "@planificadorDetalle/ActividadVisualizacion.vue";
import EtiquetaVisualizacion from "@planificadorDetalle/EtiquetaVisualizacion.vue";
import ComentarioVisualizacion from "@planificadorDetalle/ComentarioVisualizacion.vue";
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
        11: ActividadVisualizacion, // 'actividad'
        26: TareaVisualizacion, // 'tarea'
        18: EtiquetaVisualizacion, // 'etiqueta'
        13: ComentarioVisualizacion, // 'comentario'
        19: EventoVisualizacion, // 'evento'
        22: ObjetivoVisualizacion, // 'objetivo'
        21: RecurrenteVisualizacion, // 'recurrente'
        24: EventoAsociadoVisualizacion, // 'eventoasociado'
};
      return mapping[contentType] || "div";
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },

  },
};
</script>

<style scoped>
.elemento-visualizacion {
  cursor: pointer;
}

.visualizacion-container {
  flex-grow: 1;
  text-align: center;
}
</style>