<template>
  <v-card class="celda-visualizacion">
    <div class="celda-encabezado">
      <template v-if="!editing">
        <h3 class="celda-titulo" @click="enableEditing">{{ celda.contenido || '&nbsp;'  }}</h3>
      </template>
      <div v-else class="celda-edicion">
        <v-icon
          class="icono-eliminar"
          color="black"
          @click="emitirEliminarCelda"
          title="Eliminar esta celda"
        >
          mdi-minus
        </v-icon>
        <v-text-field
          v-model="editableContenido"
          dense
          solo
          flat
          class="campo-edicion"
        ></v-text-field>
        <v-icon class="icono-guardar" @click="saveChanges" title="Guardar">mdi-check</v-icon>
        <v-icon class="icono-cancelar" @click="cancelEditing" title="Cancelar">mdi-window-close</v-icon>
      </div>
    </div>

    <div v-if="elementos.length" class="celda-elementos">
      <div v-for="elemento in elementos" :key="elemento.id" class="elemento-contenedor" :style="{ backgroundColor: elemento.color, borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', padding: '10px'}">
        <ElementoVisualizacion :elemento="elemento" @elemento-desasociado="fetchElementos"/>
      </div>
    </div>

    <div v-else class="celda-sin-elementos">
      No hay elementos relacionados con esta celda.
    </div>
    <div class="anadirElemento">
      <v-icon class="icono-anadir" color="primary" @click="openAddElementDialog">mdi-plus</v-icon>
      <add-elementos
        :planificador-id="planificadorId"
        :celda-id="celda.id"
        @elemento-asociado="fetchElementos"
        ref="addElementoDialog"
      />
    </div>
  </v-card>
</template>

<script>
import ElementoVisualizacion from "@planificadorDetalle/ElementoVisualizacion.vue";
import AddElementos from "@planificadorDetalle/AddElementos.vue";
import Swal from 'sweetalert2/dist/sweetalert2';

export default {
  components: {
    ElementoVisualizacion,
    AddElementos,
  },
  props: {
    celda: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      elementos: [],
      dialog: false,
      editing: false,
      editableContenido: "",
    };
  },
  computed: {
    planificadorId() {
      return this.$route.params.id;
    },
  },
  methods: {
    openAddElementDialog() {
      this.$refs.addElementoDialog.openDialog();
    },
    enableEditing() {
      this.editableContenido = this.celda.contenido;
      this.editing = true;
    },
    cancelEditing() {
      this.editableContenido = this.celda.contenido;
      this.editing = false;
    },
    async saveChanges() {
      this.celda.contenido = this.editableContenido;
      this.editing = false;

      const requestBody = {
        contenido: this.editableContenido,
      };

      try {
        const response = await fetch(`http://localhost:8000/planificadores/${this.planificadorId}/celdas/${this.celda.id}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errorResponse = await response.json();
          Swal.fire({
            icon: 'error',
            title: 'Error al guardar',
            text: errorResponse.detail || 'No se pudo guardar el cambio.',
            showConfirmButton: true,
          });
          return;
        }
        push.success({
          title: 'Guarado!',
          message: 'El contenido de la celda fue actualizado correctamente.'
        })
      } catch {
        Swal.fire({
          icon: 'error',
          title: 'Error crítico',
          text: 'Ocurrió un problema al conectar con el servidor.',
          showConfirmButton: true,
        });
      }
    },

    async fetchElementos() {
      try {
        const response = await fetch(`http://localhost:8000/elementos/?celda=${this.celda.id}`);
        if (response.ok) {
          const data = await response.json();
          this.elementos = data.results || [];
        } else {
          Swal.fire({
            icon: 'error',
            title: 'Error al cargar',
            text: 'No se pudieron cargar los elementos relacionados.',
            showConfirmButton: true,
          });
        }
      } catch {
        Swal.fire({
          icon: 'error',
          title: 'Error crítico',
          text: 'Ocurrió un problema al conectar con el servidor.',
          showConfirmButton: true,
        });
      }
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    emitirEliminarCelda() {
      this.$emit("eliminar-celda", this.celda.id);
    },
    handleElementoCreado(elementoNuevo) {
      this.elementos.push(elementoNuevo);
      this.closeDialog();
      push.warning({
        title: 'Elemento creado',
        message: 'El nuevo elemento se agregó correctamente.',
      })
    },
  },
  async mounted() {
    await this.fetchElementos();
  },
};
</script>

<style scoped>
.celda-visualizacion {
  height: 100%;
  overflow: auto;
  border-radius: 0px;
}
.anadirElemento {
  display: flex;
  justify-content: center; /* Centrado horizontal */
  align-items: center; /* Centrado vertical */
  /* height: 100%; */
}
.celda-encabezado {
  flex: 0 0 auto;  /* No cambiar tamaño y permanecer visible */
  background-color: #f1f1f1;
  padding: 8px;
  text-align: center;
  position: sticky;
  top: 0;  /* Fijar en la parte superior de la vista */
  z-index: 100; /* Asegurar que se mantiene encima del contenido al desplazar */
}

.celda-titulo {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  color: #333;
}

.celda-edicion {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.icono-guardar {
  cursor: pointer;
  color: #4caf50; /* Verde para guardar */
  margin-left: 8px;
}

.icono-cancelar {
  cursor: pointer;
  color: #c42e2e; /* Rojo para cancelar */
  margin-left: 8px;
}

.elemento-contenedor {
  margin-bottom: 4px;
  margin-left: 4px;
  margin-right: 4px;
  color: #fff;
  font-size: 10px;
  display: flex;
  background-color: #f4f4f4;
  align-items: center; /* Centra los ítems verticalmente */
  justify-content: center; /* Centra los ítems horizontalmente */
}
.close-button {
  margin-right: auto; /* Empuja todo lo demás hacia la derecha */
}
.celda-sin-elementos {
  margin-bottom: 2px;
}
</style>
