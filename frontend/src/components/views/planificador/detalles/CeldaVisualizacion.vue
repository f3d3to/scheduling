<template>
  <v-card class="celda-visualizacion">
    <div class="celda-encabezado">
      <template v-if="!editing">
        <h3 class="celda-titulo" @click="enableEditing">{{ celda.contenido }}</h3>
      </template>
      <div v-else class="celda-edicion">
        <v-text-field
          v-model="editableContenido"
          dense
          solo
          flat
          class="campo-edicion"
        ></v-text-field>
        <v-icon class="icono-guardar" @click="saveChanges">mdi-check</v-icon>
        <v-icon class="icono-cancelar" @click="cancelEditing">mdi-close</v-icon>
      </div>
    </div>

    <div v-if="elementos.length" class="celda-elementos">
      <div v-for="elemento in elementos" :key="elemento.id" class="elemento-contenedor" :style="{ backgroundColor: elemento.color, borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', padding: '10px', marginBottom: '10px' }">
        <ElementoVisualizacion :elemento="elemento" />
      </div>
    </div>

    <div v-else class="celda-sin-elementos">
      No hay elementos relacionados con esta celda.
    </div>

  </v-card>
</template>

<script>
import ElementoVisualizacion from "@planificadorDetalle/ElementoVisualizacion.vue";
import Swal from 'sweetalert2/dist/sweetalert2';

export default {
  components: {
    ElementoVisualizacion,
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

        Swal.fire({
          icon: 'success',
          title: 'Guardado exitoso',
          text: 'El contenido de la celda fue actualizado correctamente.',
          timer: 1500,
          showConfirmButton: false,
        });
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
    handleElementoCreado(elementoNuevo) {
      this.elementos.push(elementoNuevo);
      this.closeDialog();
      Swal.fire({
        icon: 'success',
        title: 'Elemento creado',
        text: 'El nuevo elemento se agregó correctamente.',
        timer: 1500,
        showConfirmButton: false,
      });
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

.celda-encabezado {
  background-color: #f1f1f1;
  border-bottom: 2px solid #ddd;
  padding: 8px;
  text-align: center;
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
  color: #ff5252; /* Rojo para cancelar */
  margin-left: 8px;
}

.elemento-contenedor {
  margin-bottom: 10px;
  color: #fff;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  border: 1px solid #ddd; /* Borde divisorio */
  padding: 10px;
  background-color: #f4f4f4; /* Fondo claro */
}

.celda-sin-elementos {
  margin-bottom: 10px;
}
</style>
