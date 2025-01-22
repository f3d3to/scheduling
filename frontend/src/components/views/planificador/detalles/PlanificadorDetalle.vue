<template>
  <div class="planificador">
    <div class="planificador-encabezado">
      <h4 class="text-h6 font-weight-thin text-md-h5 text-lg-h4">{{ store.nombre }}
        <v-icon
          v-if="!store.isEditing"
          @click="toggleEditMode"
          class="icono-editar"
          color="blue"
          size="small"
          title="Editar planificador"
        >
          mdi-pencil
        </v-icon>
        <v-btn prepend-icon="mdi mdi-plus" v-if="store.isEditing" @click="store.showAddCeldaDialog = true">
          <template v-slot:prepend>
            <v-icon style="color:blue;"></v-icon>
          </template>
          Celda
        </v-btn>
        <v-btn prepend-icon="mdi-check-circle" v-if="store.isEditing" @click="saveLayout">
          <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>
          Guardar
        </v-btn>

        <v-btn prepend-icon="mdi mdi-window-close" v-if="store.isEditing" @click="cancelChanges">
          <template v-slot:prepend>
            <v-icon style="color: red;"></v-icon>
          </template>
          Cancelar
        </v-btn>
      </h4>
    </div>

    <div v-if="!store.layoutGenerado" class="text-h6 text-center mt-8">Cargando...</div>
    <GridLayout
      v-if="store.layoutGenerado"
      :layout="store.layout"
      :col-num="store.columnas"
      :is-draggable="store.isEditing"
      :is-resizable="store.isEditing"
      :responsive="false"
      :margin="[0, 0]"
      :auto-size="true"
      placeholder-class="grid-placeholder"
      layout-class="custom-grid-layout"
    >
      <GridItem
        v-for="item in store.layout"
        :key="item.i"
        :x="item.x"
        :y="item.y"
        :w="item.w"
        :h="item.h"
        :i="item.i"
        :class="'custom-grid-item'"
      >
        <CeldaVisualizacion
          :celda="store.getCeldaById(item.i)"
          @eliminar-celda="eliminarCelda"
        />
      </GridItem>
    </GridLayout>
    <v-dialog v-model="store.showAddCeldaDialog" max-width="600px" persistent>
      <add-celda @close-dialog="store.showAddCeldaDialog = false" @close="store.showAddCeldaDialog = false" @update-layout="handleLayoutUpdate" />
    </v-dialog>
  </div>
</template>

<script setup>
import { defineComponent, onMounted } from "vue";
import { GridLayout, GridItem } from "vue3-grid-layout-next";
import CeldaVisualizacion from "./CeldaVisualizacion.vue";
import AddCelda from "./AddCelda.vue";
import { usePlanificadorStore } from "@store/PlanificadorStore";
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import { updateConfig } from 'notivue'
import Swal from "sweetalert2";

const store = usePlanificadorStore();
const route = useRoute();
const { layoutGenerado, isEditing, nombre } = storeToRefs(store);

onMounted(async () => {
  await store.fetchData(route.params.id || "pk");
});

const toggleEditMode = () => {
  store.toggleEditMode();
  push.warning({
    title: 'Cuidado!',
    message: store.isEditing ? 'Estás en el modo edición de un planificador.' : 'Has salido del modo edición.',
  });
};

const cancelChanges = () => {
  store.cancelChanges();
  updateConfig();
  push.warning({
    title: 'Cuidado!',
    message: "Los cambios del planificador fueron cancelados!",
  });
};

const handleLayoutUpdate = async () => {
  store.handleLayoutUpdate();
  await store.fetchData(route.params.id);
};

const eliminarCelda = async (celdaId) => {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta acción eliminará permanentemente la celda y sus elementos.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#54a832",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await store.eliminarCelda(route.params.id, celdaId);
        push.success({
          title: 'Eliminada!',
          message: 'La celda fue eliminada correctamente.'
        });
      } catch (error) {
        Swal.fire("Error", error.message, "error");
      }
    }
  });
};

const saveLayout = async () => {
  try {
    await store.saveLayout(route.params.id);
    push.success({
      title: 'Guardado!',
      message: 'El diseño ha sido guardado exitosamente!',
    });
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error al guardar',
      text: 'No se pudo guardar el diseño: ' + error.message,
      confirmButtonText: 'OK'
    });
  }
};
</script>

<style scoped>
/* Mantener los estilos originales sin cambios */
.icono-editar{
  font-size: 26px;
}
.planificador-encabezado{
  text-align: center;
  margin-bottom:15px;
}

.planificador {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow: hidden;
}
.vue-grid-layout {
  background-color: #ffffff;
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