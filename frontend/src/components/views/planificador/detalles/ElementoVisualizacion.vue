<template>
  <div class="elemento-visualizacion" @click="openDialog">
    <div class="visualizacion-container">
      <span class="elemento-nombre">{{ elemento.nombre }}</span>
    </div>
    <v-dialog v-model="dialog" max-width="600px">
      <div
        v-if="elementoData"
        :style="{ backgroundColor: elementoData.color || '#6f6f6f', color: '#fff' }"
        class="elemento-dialog"
      >
        <div class="elemento-dialog-title title-container">
          <v-icon @click="desasociarElemento" class="desasociar-button" title="Eliminar de la celda">mdi-delete-circle-outline</v-icon>
          <span>{{ elementoData.nombre || elemento.nombre }}</span>
          <v-icon @click="closeDialog" class="close-button">mdi-close</v-icon>
        </div>

        <div class="elemento-dialog-content">
          <div
            v-if="elementoData.descripcion"
            class="elemento-dialog-descripcion"
          >
            {{ elementoData.descripcion }}
          </div>
          <template v-for="(value, key) in filteredData" :key="key">
            <div v-if="value" class="campo">
              <div v-if="isDateField(key)">
                <span class="campo-nombre">{{ formatKey(key) }}:</span>
                <span>{{ formatDate(value) }}</span>
              </div>
              <div v-else>
                <span class="campo-nombre">{{ formatKey(key) }}:</span>
                <span>{{ value }}</span>
              </div>
            </div>
          </template>
        </div>
      </div>
      <div v-else>Cargando...</div>
    </v-dialog>
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import { usePlanificadorStore } from '@store/PlanificadorStore';

export default {
  props: {
    elemento: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const planificadorStore = usePlanificadorStore();
    return { planificadorStore };
  },
  data() {
    return {
      dialog: false,
      elementoData: null,
    };
  },
  computed: {
    filteredData() {
      if (!this.elementoData) return {};
      const { nombre, color, descripcion, id, ...otherData } = this.elementoData;
      return otherData;
    },
  },
  methods: {
    openDialog() {
      this.dialog = true;
      this.fetchElementoData();
    },
    closeDialog() {
      this.dialog = false;
    },
    async fetchElementoData() {
      try {
        const response = await this.planificadorStore.fetchElementoDetalle(
          this.elemento.content_type,
          this.elemento.object_id
        );
        this.elementoData = response;
      } catch (error) {
        console.error("Error al obtener los datos:", error);
        this.elementoData = { error: "Error al obtener los datos" };
      }
    },
    formatKey(key) {
      return key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
    },
    formatDate(dateStr) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateStr).toLocaleDateString("es-ES", options);
    },
    isDateField(key) {
      return ["fecha_inicio", "fecha_fin", "fecha_cambio_estado",
      "fecha_actualizacion", "fecha_limite", "fecha_objetivo", "fecha_creacion",
      "fecha_hora", "proxima_fecha", "fecha_registro"].includes(key);
    },
    async desasociarElemento() {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Quieres eliminar este elemento de su celda?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#807574",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        didOpen: () => {
          const swalContainer = document.querySelector('.swal2-container');
          if (swalContainer) {
            swalContainer.style.zIndex = '10000';
          }}
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            await this.planificadorStore.eliminarElemento(this.elemento.id);
            push.success({
              title: 'Eliminado',
              message: 'El elemento ha sido eliminado correctamente.'
            });
            this.$emit('elemento-desasociado', this.elemento.id);
            this.closeDialog();
          } catch (error) {
            console.error("Error al eliminar el elemento:", error);
            Swal.fire({
              title: "Error",
              text: "No se pudo eliminar el elemento.",
              icon: "error",
              confirmButtonColor: "#54a832",
              didOpen: () => {
                const swalContainer = document.querySelector('.swal2-container');
                if (swalContainer) {
                  swalContainer.style.zIndex = '10000';
                }}
            });
          }
        }
      });
    },
  },
};
</script>

<style scoped>
.title-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.elemento-visualizacion {
  cursor: pointer;
}

.visualizacion-container {
  flex-grow: 1;
  display: grid;
  place-items: center;
}

.elemento-dialog {
  padding: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.1);
}

.elemento-dialog-title {
  font-size: 1.5em;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.elemento-dialog-content {
  margin-bottom: 20px;
}

.elemento-dialog-descripcion {
  font-style: italic;
  color: #ffffff;
  margin-bottom: 10px;
}

.campo {
  margin-bottom: 5px;
}

.campo-nombre {
  font-weight: bold;
  display: inline-block;
  min-width: 120px;
}
</style>