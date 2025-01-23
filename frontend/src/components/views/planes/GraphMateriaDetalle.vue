<template>
  <div
    v-if="selectedMateria"
    :class="['materia-detail-sidebar', { 'is-visible': isVisible }]"
  >
    <v-card class="sidebar-content">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-icon @click="closeDetail" size="small" class="close-icon">mdi-close</v-icon>
        <span class="sidebar-title">{{ selectedMateria.name }}</span>
      </v-card-title>

      <v-card-text>
        <v-tabs v-model="tab" class="sidebar-tabs">
          <v-tab value="info">Información</v-tab>
          <v-tab value="correlativas">Correlativas</v-tab>
          <v-tab value="historial">Historial</v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <!-- Pestaña de Información -->
          <v-window-item value="info">
            <v-list class="info-list">
              <v-list-item>
                <v-icon class="list-icon">mdi-calendar</v-icon>
                <v-list-item-title>Año: {{ selectedMateria.year }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-identifier</v-icon>
                <v-list-item-title>Código: {{ selectedMateria.id }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-book</v-icon>
                <v-list-item-title>Nombre: {{ selectedMateria.name }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-school</v-icon>
                <v-list-item-title>Créditos: {{ selectedMateria.metadata.creditos }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon" :class="getEstadoIconClass(selectedMateria.materiaEstudiante.estado)">
                  {{ getEstadoIcon(selectedMateria.materiaEstudiante.estado) }}
                </v-icon>
                <v-list-item-title>Estado: {{ selectedMateria.materiaEstudiante.estado }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-numeric</v-icon>
                <v-list-item-title>Nota Final: {{ selectedMateria.materiaEstudiante.nota_final }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-checkbox-marked-circle</v-icon>
                <v-list-item-title>Método de Aprobación: {{ selectedMateria.materiaEstudiante.metodo_aprobacion }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-calendar-check</v-icon>
                <v-list-item-title>Fecha de Inscripción: {{ selectedMateria.materiaEstudiante.fecha_inscripcion }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-account-group</v-icon>
                <v-list-item-title>Cátedra: {{ selectedMateria.materiaEstudiante.catedra }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-alert-circle</v-icon>
                <v-list-item-title>Dificultad: {{ selectedMateria.materiaEstudiante.dificultad }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-comment</v-icon>
                <v-list-item-title>Comentarios: {{ selectedMateria.materiaEstudiante.comentarios }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-teach</v-icon>
                <v-list-item-title>Comentarios del Docente: {{ selectedMateria.materiaEstudiante.comentarios_docente }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-window-item>

          <!-- Pestaña de Correlativas -->
          <v-window-item value="correlativas">
            <v-list class="correlativas-list">
              <v-list-item
                v-for="correlativa in selectedMateria.metadata.correlativas"
                :key="correlativa"
              >
                <v-icon class="list-icon">mdi-link</v-icon>
                <v-list-item-title>{{ correlativa }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-window-item>

          <!-- Pestaña de Historial -->
          <v-window-item value="historial">
            <v-list class="historial-list">
              <v-list-item>
                <v-icon class="list-icon">mdi-repeat</v-icon>
                <v-list-item-title>Intentos: {{ selectedMateria.materiaEstudiante.intentos }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-update</v-icon>
                <v-list-item-title>Última Actualización: {{ selectedMateria.materiaEstudiante.fecha_actualizacion }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  name: "GraphMateriaDetalle",
  props: {
    selectedMateria: {
      type: Object,
      default: null,
    },
  },
  setup(props) {
    const isVisible = ref(false);

    // Abrir el sidebar cuando se selecciona una materia
    watch(
      () => props.selectedMateria,
      (newVal) => {
        isVisible.value = !!newVal;
      }
    );

    return { isVisible };
  },
  data() {
    return {
      tab: "info", // Pestaña activa por defecto
    };
  },
  methods: {
    closeDetail() {
      this.$emit("close-detail");
      this.isVisible = false; // Cerrar el sidebar
    },
    getEstadoIcon(estado) {
      switch (estado) {
        case "promocionada":
          return "mdi-star"; // Icono para "Promocionada"
        case "aprobada":
          return "mdi-check"; // Icono para "Aprobada"
        case "cursando":
          return "mdi-progress-check"; // Icono para "Cursando"
        case "pendiente":
          return "mdi-clock-alert"; // Icono para "Pendiente"
        case "desaprobada":
          return "mdi-alert"; // Icono para "Desaprobada"
        default:
          return "mdi-alert"; // Icono por defecto
      }
    },
    getEstadoIconClass(estado) {
      switch (estado) {
        case "promocionada":
          return "icon-promocionada"; // Clase para "Promocionada"
        case "aprobada":
          return "icon-aprobada"; // Clase para "Aprobada"
        case "cursando":
          return "icon-cursando"; // Clase para "Cursando"
        case "pendiente":
          return "icon-pendiente"; // Clase para "Pendiente"
        case "desaprobada":
          return "icon-desaprobada"; // Clase para "Desaprobada"
        default:
          return "icon-default"; // Clase por defecto
      }
    },
  },
});
</script>

<style scoped>
.materia-detail-sidebar {
  position: fixed;
  top: 0;
  right: -400px; /* Inicialmente oculto */
  width: 400px;
  height: 100vh;
  background: linear-gradient(90deg, #2c2c3e, #1e1e2f);
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.2);
  transition: right 0.3s ease;
  z-index: 1000;
}

.materia-detail-sidebar.is-visible {
  right: 0; /* Mostrar el sidebar */
}

.sidebar-content {
  height: 100%;
  overflow-y: auto;
  background-color: #1e1e2f;
  color: white;
}

.sidebar-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 1rem;
  font-weight: bold;
  color: white;
}

.close-icon {
  color: white;
  cursor: pointer;
}

.sidebar-tabs {
  background-color: #2c2c3e;
}

.info-list,
.correlativas-list,
.historial-list {
  background-color: #1e1e2f;
  color: white;
}

.list-icon {
  margin-right: 10px;
  color: #535bf2;
}

.icon-promocionada {
  color: #ffeb3b; /* Amarillo para "Promocionada" */
}

.icon-aprobada {
  color: #4caf50; /* Verde para "Aprobada" */
}

.icon-cursando {
  color: #2196f3; /* Azul para "Cursando" */
}

.icon-pendiente {
  color: #ff9800; /* Naranja para "Pendiente" */
}

.icon-desaprobada {
  color: #f44336; /* Rojo para "Desaprobada" */
}

.icon-default {
  color: #9e9e9e; /* Gris por defecto */
}
</style>