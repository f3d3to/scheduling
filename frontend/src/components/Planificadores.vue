<template>
  <v-container>
    <div class="text-h5 mb-4 text-center">Iniciar un nuevo planificador</div>
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="8">
        <v-row v-if="templates && templates.length" justify="center">
          <v-col cols="12" md="4" v-for="template in templates" :key="template.id">
            <v-card class="template-card" @click="createNewFromTemplate(template)">
              <v-img :src="template.configuracion?.imagen || 'https://via.placeholder.com/150'" height="150px" cover></v-img>
              <v-card-title class="text-subtitle-2 text-center">{{ template.nombre }}</v-card-title>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="template-card" @click="showCreateModal">
              <v-img src="https://via.placeholder.com/150" height="150px" cover></v-img>
              <v-card-title class="text-subtitle-2 text-center">
                <v-icon large>mdi-plus-circle</v-icon>
                <span>Agregar planificador</span>
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
        <div v-else class="text-h6 text-center mt-4">No hay tipos de planificadores disponibles.</div>
      </v-col>
    </v-row>

    <div class="text-h5 mt-8 mb-4 text-center">Planificadores recientes</div>
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="8">
        <v-row justify="center">
          <v-col cols="12" md="4" v-for="planner in planners" :key="planner.id">
            <v-card class="planner-card">
              <v-card-title class="text-subtitle-1 text-center">{{ planner.nombre }}</v-card-title>
              <v-card-subtitle class="text-center">
                Última modificación: {{ planner.fecha_modificacion ? formatDate(planner.fecha_modificacion) : 'Desconocida' }}
              </v-card-subtitle>
              <v-card-actions class="justify-center">
                <v-btn variant="text" color="primary" @click="redirectToDetail(planner)">Abrir</v-btn>
                <v-menu location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn icon v-bind="props">
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="showEditModal(planner)">
                      <v-list-item-title>Editar</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="deletePlanner(planner)">
                      <v-list-item-title>Eliminar</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <div v-if="!planners || !planners.length" class="text-h6 text-center mt-8">No hay planificadores disponibles. Crea uno nuevo para comenzar.</div>
      </v-col>
    </v-row>

    <!-- Modal para crear/editar planificadores -->
    <v-dialog v-model="modalVisible" max-width="500px">
      <v-card>
        <v-card-title class="text-center">
          {{ isEditing ? 'Editar Planificador' : 'Crear Nuevo Planificador' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field label="Nombre" v-model="formData.nombre" required></v-text-field>
            <v-select
              label="Tipo"
              :items="templateTypes"
              v-model="formData.tipo"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn color="primary" @click="savePlanner">Guardar</v-btn>
          <v-btn text @click="closeModal">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>


<script>
export default {
  name: 'PlannerDashboard',
  data() {
    return {
      planners: [],
      templates: [],
      templateTypes: [],
      modalVisible: false,
      isEditing: false,
      currentPlanner: null,
      formData: {
        nombre: '',
        tipo: '',
      },
    };
  },
  mounted() {
    this.fetchPlanners();
    this.fetchTemplates();
  },
  methods: {
    async fetchPlanners() {
      try {
        const response = await fetch('http://localhost:8000/planificadores/');
        if (!response.ok) {
          throw new Error('Error al cargar los planificadores');
        }
        const data = await response.json();
        this.planners = data.results || [];
      } catch (error) {
        console.error('Error al obtener planificadores:', error);
        this.planners = [];
      }
    },
    async fetchTemplates() {
      try {
        const response = await fetch('http://localhost:8000/estructuras-planificador/');
        if (!response.ok) {
          throw new Error('Error al cargar los tipos de planificadores');
        }
        const data = await response.json();
        this.templates = data.results || [];
        this.templateTypes = this.templates.map(template => template.nombre);
      } catch (error) {
        console.error('Error al obtener tipos de planificadores:', error);
        this.templates = [];
        this.templateTypes = [];
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES');
    },
    redirectToDetail(planner) {
      this.$router.push({ name: 'PlanificadorDetalle', params: { id: planner.id } });
    },
    showCreateModal() {
      this.isEditing = false;
      this.formData = { nombre: '', tipo: '' };
      this.modalVisible = true;
    },
    showEditModal(planner) {
      this.isEditing = true;
      this.currentPlanner = planner;
      this.formData = { nombre: planner.nombre, tipo: planner.tipo };
      this.modalVisible = true;
    },
    closeModal() {
      this.modalVisible = false;
      this.formData = { nombre: '', tipo: '' };
      this.currentPlanner = null;
    },
    async savePlanner() {
      try {
        const url = this.isEditing
          ? `http://localhost:8000/planificadores/${this.currentPlanner.id}/`
          : 'http://localhost:8000/planificadores/';
        const method = this.isEditing ? 'PATCH' : 'POST';

        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });

        if (!response.ok) {
          throw new Error(this.isEditing ? 'Error al editar el planificador' : 'Error al crear el planificador');
        }

        this.fetchPlanners();
        this.closeModal();
      } catch (error) {
        console.error(this.isEditing ? 'Error al editar planificador:' : 'Error al crear planificador:', error);
      }
    },
    async createNewFromTemplate(template) {
      try {
        const response = await fetch('http://localhost:8000/planificadores/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ nombre: `Planificador - ${template.nombre}`, tipo: template.nombre, estructura: template.id }),
        });
        if (!response.ok) {
          throw new Error('Error al crear el planificador desde plantilla');
        }
        this.fetchPlanners();
      } catch (error) {
        console.error('Error al crear planificador desde plantilla:', error);
      }
    },
    async deletePlanner(planner) {
      try {
        const response = await fetch(`http://localhost:8000/planificadores-eliminar/${planner.id}/`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error('Error al eliminar el planificador');
        }
        this.fetchPlanners();
      } catch (error) {
        console.error('Error al eliminar planificador:', error);
      }
    },
  },
};
</script>

<style scoped>
.template-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #ccc;
  padding: 10px;
}

.template-card:hover {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.planner-card {
  transition: all 0.3s ease;
}

.planner-card:hover {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
