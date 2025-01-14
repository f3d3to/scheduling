<template>
  <div class="planificador">
    <div class="planificador-encabezado">
      <h4 class="text-h6 font-weight-thin text-md-h5 text-lg-h4">{{ nombre  }}
      <v-btn prepend-icon="mdi mdi-pencil" v-if="!isEditing" @click="toggleEditMode">
        <template v-slot:prepend><v-icon style="color:blue;" ></v-icon></template>
      </v-btn>
      <v-btn prepend-icon="mdi mdi-plus" v-if="isEditing" @click="showAddCeldaDialog = true">
        <template v-slot:prepend>
          <v-icon style="color:blue;" ></v-icon>
        </template>
        Celda
      </v-btn>
      <v-btn prepend-icon="mdi-check-circle" v-if="isEditing" @click="saveLayout">
        <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>
        Guardar
      </v-btn>

      <v-btn prepend-icon="mdi mdi-window-close" v-if="isEditing" @click="cancelChanges">
        <template v-slot:prepend>
            <v-icon style="color: red;" ></v-icon>
          </template>
        Cancelar
      </v-btn>
    </h4>
    </div>

    <div v-if="!layoutGenerado" class="text-h6 text-center mt-8">Cargando...</div>
    <GridLayout
      v-if="layoutGenerado"
      :layout="layout"
      :col-num="columnas"
      :is-draggable="isEditing"
      :is-resizable="isEditing"
      :responsive="false"
      :margin="[0, 0]"
      :auto-size="true"
      @layout-updated="onLayoutUpdated"

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
    <v-dialog v-model="showAddCeldaDialog" max-width="600px" persistent>
      <add-celda @close-dialog="showAddCeldaDialog = false" @close="showAddCeldaDialog = false" />
    </v-dialog>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { GridLayout, GridItem } from "vue3-grid-layout-next";
import CeldaVisualizacion from "./CeldaVisualizacion.vue";
import AddCelda from "./AddCelda.vue";
import Swal from 'sweetalert2/dist/sweetalert2';

export default defineComponent({
  components: {
    GridLayout,
    GridItem,
    CeldaVisualizacion,
    AddCelda
  },
  data() {
    return {
      layout: [],
      celdas: [],
      columnas: 7,
      layoutGenerado: false,
      isEditing: false,
      nombre:"",
      showAddCeldaDialog: false,
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
        this.nombre = data.nombre;
      }
    },
    generateLayout(celdas) {
      return celdas.map((celda) => {
        const [fila, columna] = celda.coordenadas.split(",").map(Number);
        return { i: String(celda.id), x: columna - 1, y: fila - 1, w: celda.w, h: celda.h };
      });
    },
    getCeldaById(id) {
      return this.celdas.find((celda) => celda.id === parseInt(id));
    },
    cancelChanges() {
      this.layout = JSON.parse(JSON.stringify(this.originalLayout)); // Restaurar el layout original
      this.isEditing = false;
      Swal.fire({
        icon: 'info',
        title: 'Cambios Cancelados',
        text: 'Todos los cambios no guardados han sido descartados.',
        confirmButtonText: 'OK'
      });
    },
    onLayoutUpdated(newLayout) {
    },
    toggleEditMode() {
      if (!this.isEditing) {
        this.originalLayout = JSON.parse(JSON.stringify(this.layout));
      } else {
        this.layout = this.originalLayout;
      }
      this.isEditing = !this.isEditing;
      Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: true,
        icon: 'info',
        title: 'Edición',
        text: this.isEditing ? 'Estás en el modo edición de un planificador.' : 'Has salido del modo edición.'
      });
    },
  async saveLayout() {
    let tablaActualizada = {};
    this.layout.forEach(({ i, x, y }) => {
      let celda = this.getCeldaById(i);
      tablaActualizada[`${y + 1},${x + 1}`] = { id: celda.id, contenido: celda.contenido, w: celda.w, h: celda.h };
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
.planificador-encabezado{
  text-align: center;

  margin-bottom:15px;
}

.planificador {
  display: flex;
  flex-direction: column;
  height: 100%; /* Ocupa todo el espacio disponible */
  width: 100%; /* Usa todo el ancho del contenedor */
  overflow: hidden; /* Evita scroll no deseado */
}
.vue-grid-layout {
  background-color: #ffffff;
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