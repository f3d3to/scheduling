<template>
  <v-card class="celda-visualizacion">
    <v-list-item-title>
      <v-icon @click="openDialog">mdi-plus</v-icon> <!-- Ícono para agregar elementos -->
      {{ celda.contenido }}
      {{ celda.id }}

    </v-list-item-title>

    <!-- Contenedor de Elementos -->
    <div v-if="elementos.length" class="celda-elementos">
      <div v-for="elemento in elementos" :key="elemento.id" class="elemento-contenedor">
        {{ elemento.nombre }}
      </div>
    </div>
    <div v-else class="celda-sin-elementos">
      No hay elementos relacionados con esta celda.
    </div>

    <!-- Diálogo para Crear Nuevo Elemento -->
    <v-dialog v-model="dialog" max-width="600px">
      <CrearElemento :celdaId="celda.id" @elemento-creado="handleElementoCreado" @cancelar="closeDialog" />
    </v-dialog>
  </v-card>
</template>

<script>
import ElementoVisualizacion from "@planificadorDetalle/ElementoVisualizacion.vue";
import CrearElemento from "@planificadorDetalle/CrearElemento.vue";

export default {
  props: {
    celda: {
      type: Object,
      required: true,
    },
  },
  components: {
    ElementoVisualizacion,
    CrearElemento,
  },
  data() {
    return {
      elementos: [],
      dialog: false,
    };
  },
  methods: {
    async fetchElementos() {
      try {
        const response = await fetch(`http://localhost:8000/elementos/?celda=${this.celda.id}`);
        if (response.ok) {
          const data = await response.json();
          this.elementos = data.results || [];
        } else {
          console.error("Error al cargar los elementos:", response.statusText);
        }
      } catch (error) {
        console.error("Error al hacer fetch de los elementos:", error);
      }
    },
    actualizarElementoEnLista(elementoActualizado) {
      const index = this.elementos.findIndex(el => el.id === elementoActualizado.id);
      if (index !== -1) {
        this.elementos.splice(index, 1, elementoActualizado);
      }
    },
    eliminarElementoDeLista(elementoId) {
      this.elementos = this.elementos.filter(el => el.id !== elementoId);
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    handleElementoCreado(elementoNuevo) {
      this.elementos.push(elementoNuevo);
      this.closeDialog();
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
