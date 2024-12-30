<template>
  <div class="planificador">
    <GridLayout
      v-if="layoutGenerado"
      :layout="layout"
      :col-num="columnas"
      :is-draggable="isEditing"
      :is-resizable="false"
      :responsive="false"
      :margin="[0, 0]"
      :auto-size="true"
      placeholder-class="grid-placeholder"
      layout-class="custom-grid-layout"
    >
      <GridItem
        v-for="item in layout"
        :key="item.i"
        :x="item.x"
        :y="item.y"
        :w="item.w"
        :h="item.h"
        :i="item.i"
        :class="'custom-grid-item'"
      >
        <CeldaVisualizacion :celda="getCeldaById(item.i)" />
      </GridItem>
    </GridLayout>
  </div>
  <button  v-if="!isEditing" class="btn btn-editar" @click="toggleEditMode">Editar</button>
    <button v-if="isEditing" class="btn btn-guardar" @click="saveLayout">Guardar</button>

</template>

<script>
import { defineComponent } from "vue";
import { GridLayout, GridItem } from "vue3-grid-layout-next";
import CeldaVisualizacion from "./CeldaVisualizacion.vue";
import Swal from 'sweetalert2/dist/sweetalert2';

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
      columnas: 7,
      layoutGenerado: false,
      isEditing: false,
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      const planificadorId = this.$route.params.id || "pk";
      const response = await fetch(`http://localhost:8000/estructuras-planificador/${planificadorId}/`);
      if (response.ok) {
        const data = await response.json();
        this.columnas = data.columnas;
        this.celdas = Object.entries(data.tabla).map(([coordenadas, celda]) => ({...celda, coordenadas}));
        this.layout = this.generateLayout(this.celdas);
        this.layoutGenerado = true;
      }
    },
    generateLayout(celdas) {
      return celdas.map((celda) => {
        const [fila, columna] = celda.coordenadas.split(",").map(Number);
        return { i: String(celda.id), x: columna - 1, y: fila - 1, w: 1, h: 1.8 };
      });
    },
    getCeldaById(id) {
      return this.celdas.find((celda) => celda.id === parseInt(id));
    },
    toggleEditMode() {
      Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: true,
        icon: 'info',
        title: 'Edición',
        text: 'Estás en el modo edición de un planificador.'
      });
      this.isEditing = !this.isEditing;
    },

    async saveLayout() {
  let tablaActualizada = {};
  this.layout.forEach(({ i, x, y }) => {
    let celda = this.getCeldaById(i);
    tablaActualizada[`${y + 1},${x + 1}`] = { id: celda.id, contenido: celda.contenido };
  });
  const requestBody = {
    id: this.$route.params.id,
    tabla: tablaActualizada,
    nombre: this.nombrePlanificador,
    configuracion: {
      tipo: "tabla",
      filas: this.filas,
      columnas: this.columnas
    },
    filas: this.filas,
    columnas: this.columnas,
    ancho_columna: this.anchoColumna
  };

  try {
    const response = await fetch(`http://localhost:8000/estructuras-planificador/${this.$route.params.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) throw new Error('Failed to save layout');
    Swal.fire({
      icon: 'success',
      title: 'Guardado',
      text: 'El diseño ha sido guardado exitosamente!',
      confirmButtonText: 'OK'
    });
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error al guardar',
      text: 'No se pudo guardar el diseño: ' + error.message,
      confirmButtonText: 'OK'
    });  }
  this.isEditing = false;
}

  },
});
</script>

<style scoped>
.planificador {
  display: flex;
  flex-direction: column;
  height: 100%; /* Ocupa todo el espacio disponible */
  width: 100%; /* Usa todo el ancho del contenedor */
  overflow: hidden; /* Evita scroll no deseado */
}
.vue-grid-layout {
  background-color: #8d3535;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

}

.grid-item {
  width: 100%;
  overflow: hidden;
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
.vue-grid-item.vue-grid-placeholder {
  background: green !important;
}

</style>