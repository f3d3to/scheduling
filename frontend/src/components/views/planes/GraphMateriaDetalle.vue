<template>
  <div
    v-if="selectedMateria"
    :class="['materia-detail-sidebar', { 'is-visible': isVisible }]"
  >
    <v-card class="sidebar-content">
      <v-card-title class="d-flex justify-space-between align-center">
        <v-icon @click="closeDetail" size="small" class="close-icon">mdi-close</v-icon>
        <span class="sidebar-title">{{ selectedMateria.name }}</span>
        <div>
          <v-icon v-if="isEditMode" @click="cancelEdit" class="cancel-icon">mdi-undo</v-icon>
          <v-icon v-if="selectedMateria.materiaEstudiante" @click="toggleEditMode" class="edit-icon">
            {{ isEditMode ? 'mdi-content-save' : 'mdi-pencil' }}
          </v-icon>
          <v-icon v-if="!selectedMateria.materiaEstudiante" @click="openCreateForm" class="add-icon">mdi-plus</v-icon>
        </div>
      </v-card-title>

      <v-card-text>
        <v-tabs v-model="tab" class="sidebar-tabs">
          <v-tab value="info">Información</v-tab>
          <v-tab value="correlativas">Correlativas</v-tab>
          <v-tab v-if="selectedMateria.materiaEstudiante" value="historial">Historial</v-tab>
          <v-tab value="personalizar">Personalizar</v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <!-- Pestaña de Información -->
          <v-window-item value="info">
            <v-list class="info-list">
              <v-list-item>
                <v-icon class="list-icon">mdi-calendar</v-icon>
                <v-list-item-title>
                  Año:
                  <span v-if="!isEditMode">{{ selectedMateria.year }}</span>
                  <v-text-field v-else v-model="editableMateria.year" dense></v-text-field>
                </v-list-item-title>
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
                <v-list-item-title>
                  Créditos:
                  <span v-if="!isEditMode">{{ selectedMateria.metadata.creditos }}</span>
                  <v-text-field v-else v-model="editableMateria.creditos" dense></v-text-field>
                </v-list-item-title>
              </v-list-item>

              <!-- Campos que dependen de materiaEstudiante -->
              <template v-if="selectedMateria.materiaEstudiante">
                <v-list-item>
                  <v-icon class="list-icon" :class="getEstadoIconClass(editableMateria.estado)">
                    {{ getEstadoIcon(editableMateria.estado) }}
                  </v-icon>
                  <v-list-item-title>
                    Estado:
                    <span v-if="!isEditMode">{{ editableMateria.estado }}</span>
                    <v-select v-else v-model="editableMateria.estado" :items="estados" dense></v-select>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-numeric</v-icon>
                  <v-list-item-title>
                    Nota Final:
                    <span v-if="!isEditMode">{{ editableMateria.nota_final }}</span>
                    <v-text-field v-else v-model="editableMateria.nota_final" dense></v-text-field>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-checkbox-marked-circle</v-icon>
                  <v-list-item-title>
                    Método de Aprobación:
                    <span v-if="!isEditMode">{{ editableMateria.metodo_aprobacion }}</span>
                    <v-select v-else v-model="editableMateria.metodo_aprobacion" :items="metodosAprobacion" dense></v-select>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-calendar-check</v-icon>
                  <v-list-item-title>
                    Fecha de Inscripción:
                    <span v-if="!isEditMode">{{ editableMateria.fecha_inscripcion }}</span>
                    <v-text-field v-else v-model="editableMateria.fecha_inscripcion" dense type="date"></v-text-field>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-account-group</v-icon>
                  <v-list-item-title>
                    Cátedra:
                    <span v-if="!isEditMode">{{ editableMateria.catedra }}</span>
                    <v-text-field v-else v-model="editableMateria.catedra" dense></v-text-field>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-alert-circle</v-icon>
                  <v-list-item-title>
                    Dificultad:
                    <span v-if="!isEditMode">{{ editableMateria.dificultad }}</span>
                    <v-text-field v-else v-model="editableMateria.dificultad" dense></v-text-field>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-comment</v-icon>
                  <v-list-item-title>
                    Comentarios:
                    <span v-if="!isEditMode">{{ editableMateria.comentarios }}</span>
                    <v-textarea v-else v-model="editableMateria.comentarios" dense></v-textarea>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-icon class="list-icon">mdi-teach</v-icon>
                  <v-list-item-title>
                    Comentarios del Docente:
                    <span v-if="!isEditMode">{{ editableMateria.comentarios_docente }}</span>
                    <v-textarea v-else v-model="editableMateria.comentarios_docente" dense></v-textarea>
                  </v-list-item-title>
                </v-list-item>
              </template>
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

          <!-- Pestaña de Historial (solo visible si existe materiaEstudiante) -->
          <v-window-item v-if="selectedMateria.materiaEstudiante" value="historial">
            <v-list class="historial-list">
              <v-list-item>
                <v-icon class="list-icon">mdi-repeat</v-icon>
                <v-list-item-title>Intentos: {{ editableMateria.intentos || 0 }}</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-icon class="list-icon">mdi-update</v-icon>
                <v-list-item-title>Última Actualización: {{ editableMateria.fecha_actualizacion || 'N/A' }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-window-item>

          <!-- Pestaña de Personalizar -->
          <v-window-item value="personalizar">
            <v-list class="personalizar-list">
              <v-list-item>
                <v-icon class="list-icon">mdi-palette</v-icon>
                <v-list-item-title>Color Personalizado</v-list-item-title>
                <input type="color" v-model="customColor" @change="updateNodeColor" />
              </v-list-item>
            </v-list>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    <!-- Diálogo para crear materiaEstudiante -->
    <v-dialog v-model="isCreateFormVisible" max-width="600">
      <MateriaEstudianteForm
        v-if="isCreateFormVisible"
        :materia="selectedMateria"
        @close="closeCreateForm"
        @materia-estudiante-created="handleMateriaEstudianteCreated"
      />
    </v-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from "vue";
import { useGraphStore } from "@store/GraphStore";
import MateriaEstudianteForm from "./MateriaEstudianteForm.vue";

export default defineComponent({
  name: "GraphMateriaDetalle",
  components: {
    MateriaEstudianteForm,
  },
  props: {
    selectedMateria: {
      type: Object,
      default: null,
    },
  },
  setup(props) {
    const isVisible = ref(false);
    const isEditMode = ref(false);
    const estados = ref(['pendiente', 'cursando', 'aprobada', 'desaprobada', 'promocionada']);
    const metodosAprobacion = ref(['final', 'promocion', 'equivalencia']);
    const graphStore = useGraphStore();

    // Inicializar con valores por defecto
    const editableMateria = ref({
      estado: '',
      nota_final: '',
      metodo_aprobacion: '',
      fecha_inscripcion: '',
      catedra: '',
      dificultad: '',
      comentarios: '',
      comentarios_docente: '',
      intentos: 0,
      fecha_actualizacion: '',
      creditos: 0,
    });

    watch(
      () => props.selectedMateria,
      (newVal) => {
        isVisible.value = !!newVal;
        if (newVal) {
          // Fusionar con valores por defecto si materiaEstudiante no existe
          const materiaEstudiante = newVal.materiaEstudiante || {};
          editableMateria.value = {
            ...editableMateria.value, // Mantener valores por defecto
            ...materiaEstudiante,
            creditos: newVal.metadata?.creditos || 0
          };
        }
      }
    );

    const toggleEditMode = async () => {
      if (isEditMode.value) {
        await graphStore.updateMateriaEstudiante(editableMateria.value);
      }
      isEditMode.value = !isEditMode.value;
    };

    const cancelEdit = () => {
      isEditMode.value = false;
      editableMateria.value = {
        ...editableMateria.value,
        ...(props.selectedMateria?.materiaEstudiante || {})
      };
    };

    return {
      isVisible,
      isEditMode,
      editableMateria,
      estados,
      metodosAprobacion,
      toggleEditMode,
      cancelEdit,
    };
  },
  data() {
    return {
      tab: "info",
      customColor: '',
      isCreateFormVisible: false,
    };
  },
  methods: {
    closeDetail() {
      this.$emit("close-detail");
      this.isVisible = false;
    },
    getEstadoIcon(estado) {
      switch (estado) {
        case "promocionada":
          return "mdi-star";
        case "aprobada":
          return "mdi-check";
        case "cursando":
          return "mdi-progress-check";
        case "pendiente":
          return "mdi-clock-alert";
        case "desaprobada":
          return "mdi-alert";
        default:
          return "mdi-alert";
      }
    },
    getEstadoIconClass(estado) {
      switch (estado) {
        case "promocionada":
          return "icon-promocionada";
        case "aprobada":
          return "icon-aprobada";
        case "cursando":
          return "icon-cursando";
        case "pendiente":
          return "icon-pendiente";
        case "desaprobada":
          return "icon-desaprobada";
        default:
          return "icon-default";
      }
    },
    updateNodeColor() {
      this.$emit("update-node-color", this.selectedMateria.id, this.customColor);
    },
    openCreateForm() {
      this.isCreateFormVisible = true;
    },

    closeCreateForm() {
      this.isCreateFormVisible = false;
      this.$emit("close-detail");
    },
    handleMateriaEstudianteCreated(nuevaMateriaEstudiante) {
    this.selectedMateria.materiaEstudiante = nuevaMateriaEstudiante;
    this.closeCreateForm();
    }
  },
});
</script>

<style scoped>
/* Estilos sin cambios */
.materia-detail-sidebar {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: linear-gradient(90deg, #2c2c3e, #1e1e2f);
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.2);
  transition: right 0.3s ease;
  z-index: 1000;
}

.materia-detail-sidebar.is-visible {
  right: 0;
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
.historial-list,
.personalizar-list {
  background-color: #1e1e2f;
  color: white;
}

.list-icon {
  margin-right: 10px;
  color: #535bf2;
}

.icon-promocionada {
  color: #ffeb3b;
}

.icon-aprobada {
  color: #4caf50;
}

.icon-cursando {
  color: #2196f3;
}

.icon-pendiente {
  color: #ff9800;
}

.icon-desaprobada {
  color: #f44336;
}

.icon-default {
  color: #9e9e9e;
}

input[type="color"] {
  margin-left: 10px;
  cursor: pointer;
}

.edit-icon, .cancel-icon {
  cursor: pointer;
  color: white;
  margin-left: 10px;
}
.add-icon {
  cursor: pointer;
  color: white;
  margin-left: 10px;
}
</style>