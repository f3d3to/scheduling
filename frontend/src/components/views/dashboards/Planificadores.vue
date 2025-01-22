<!-- PlannerDashboard.vue -->
<template>
  <v-container>
    <div class="text-h5 mb-4 text-center">Iniciar un nuevo planificador</div>
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="8">
        <v-row v-if="store.templates.length" justify="center">
          <v-col cols="12" md="4" v-for="template in store.templates" :key="template.id">
            <v-card class="template-card" @click="createFromTemplate(template)">
              <v-img :src="template.configuracion?.imagen || 'https://via.placeholder.com/150'" height="150px" cover></v-img>
              <v-card-title class="text-subtitle-2 text-center">{{ template.nombre }}</v-card-title>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="template-card" @click="store.toggleModal(false)">
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
          <v-col cols="12" md="4" v-for="planner in store.planners" :key="planner.id">
            <v-card class="planner-card">
              <v-card-title class="text-subtitle-1 text-center">{{ planner.nombre }}</v-card-title>
              <v-card-subtitle class="text-center">
                Última modificación: {{ formatDate(planner.fecha_modificacion) }}
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
                    <v-list-item @click="store.toggleModal(true, planner)">
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
        <div v-if="!store.planners.length" class="text-h6 text-center mt-8">
          No hay planificadores disponibles. Crea uno nuevo para comenzar.
        </div>
      </v-col>
    </v-row>

    <!-- Modal para crear/editar planificadores -->
    <v-dialog v-model="store.modalVisible" max-width="500px">
      <v-card>
        <v-card-title class="text-center">
          {{ store.isEditing ? 'Editar Planificador' : 'Crear Nuevo Planificador' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field label="Nombre" v-model="store.formData.nombre" required></v-text-field>
            <v-select
              label="Tipo"
              :items="store.templateTypes"
              v-model="store.formData.tipo"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn color="primary" @click="savePlanner">Guardar</v-btn>
          <v-btn text @click="store.closeModal">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { usePlanificadorStore } from "@store/PlanificadorStore";
import Swal from 'sweetalert2';

const store = usePlanificadorStore();
const router = useRouter();

onMounted(async () => {
  await Promise.all([store.fetchPlanners(), store.fetchTemplates()]);
});

const formatDate = (dateString) => {
  if (!dateString) return 'Desconocida';
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES');
};

const redirectToDetail = (planner) => {
  router.push({ name: 'PlanificadorDetalle', params: { id: planner.id } });
};

const createFromTemplate = async (template) => {
  try {
    await store.createFromTemplate(template.id, template.nombre);
    Swal.fire('Éxito', 'Planificador creado correctamente', 'success');
  } catch (error) {
    Swal.fire('Error', 'No se pudo crear el planificador', 'error');
  }
};

const deletePlanner = async (planner) => {
  try {
    await Swal.fire({
      title: '¿Estás seguro?',
      text: "¡No podrás revertir esta acción!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar!'
    });

    await store.deletePlanner(planner.id);
    Swal.fire('Eliminado!', 'El planificador ha sido eliminado.', 'success');
  } catch (error) {
    Swal.fire('Cancelado', 'Tu planificador está seguro :)', 'info');
  }
};

const savePlanner = async () => {
  try {
    if (store.isEditing && store.currentPlanner) {
      await store.updatePlanner(store.currentPlanner.id, store.formData);
    } else {
      await store.createPlanner(store.formData);
    }
    Swal.fire('Éxito', 'Operación realizada correctamente', 'success');
    store.closeModal();
  } catch (error) {
    Swal.fire('Error', 'Ocurrió un error durante la operación', 'error');
  }
};
</script>

<style scoped>
/* Mantener los mismos estilos */
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