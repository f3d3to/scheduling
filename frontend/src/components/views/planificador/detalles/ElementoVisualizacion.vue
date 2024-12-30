<template>
    <div class="elemento-visualizacion">
      <component
        :is="getComponent(elemento.content_type)"
        :elemento="elemento"
      />
    </div>
</template>

  <script>
  import TareaVisualizacion from "./TareaVisualizacion.vue";
  import ActividadVisualizacion from "./ActividadVisualizacion.vue";

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
    },
    methods: {
      getComponent(contentType) {
        const mapping = {
          8: "ActividadVisualizacion",
          9: "TareaVisualizacion",
        };
        return mapping[contentType] || "div";
      },
    },
  };
  </script>

  <style scoped>
  .elemento-visualizacion {
    /* Estilos propios del contenedor del elemento */
  }
  </style>