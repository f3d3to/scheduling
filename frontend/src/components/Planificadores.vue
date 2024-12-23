<template>
  <v-container>
    <!-- Vista Principal de Planificadores -->
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card>
          <v-card-title class="headline">Gestión de Planificadores</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="4" v-for="planificador in planificadores" :key="planificador.id">
                <v-card outlined>
                  <v-card-title>{{ planificador.nombre }}</v-card-title>
                  <v-card-subtitle>{{ planificador.tipo }}</v-card-subtitle>
                  <v-card-actions>
                    <v-btn icon color="blue" @click="editPlanificador(planificador)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon color="red" @click="deletePlanificador(planificador.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
            <v-alert v-if="planificadores.length === 0" type="info" border="left" color="blue" dark>
              No hay planificadores disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Planificador</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Diálogo para añadir/editar planificador -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Planificador</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.nombre" label="Nombre del Planificador" outlined required></v-text-field>
          <v-text-field v-model="form.tipo" label="Tipo de Planificador" outlined required></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="savePlanificador">Guardar</v-btn>
          <v-btn text color="error" @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const planificadores = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  tipo: "",
});

// Funciones para interactuar con la API
async function fetchPlanificadores() {
  try {
    const response = await fetch("http://localhost:8000/planificadores/");
    if (response.ok) {
      const data = await response.json();
      planificadores.value = data.results || data; // Ajusta esto según la estructura de respuesta de tu API
    } else {
      console.error("Error al obtener planificadores:", response.status);
      planificadores.value = [];
    }
  } catch (error) {
    console.error("Error en fetchPlanificadores:", error);
    planificadores.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, nombre: "", tipo: "" };
  dialog.value = true;
}

function editPlanificador(planificador) {
  dialogMode.value = "edit";
  form.value = { ...planificador };
  dialog.value = true;
}

async function savePlanificador() {
  const method = dialogMode.value === "add" ? "POST" : "PUT";
  const url = dialogMode.value === "add" ? "http://localhost:8000/planificadores/" : `http://localhost:8000/planificadores/${form.value.id}/`;
  const response = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form.value),
  });

  if (response.ok) {
    fetchPlanificadores();
    dialog.value = false;
  } else {
    console.error("Error al guardar planificador:", response.status);
  }
}

async function deletePlanificador(id) {
  const response = await fetch(`http://localhost:8000/planificadores/${id}/`, { method: "DELETE" });

  if (response.ok) {
    fetchPlanificadores();
  } else {
    console.error("Error al eliminar planificador:", response.status);
  }
}

onMounted(() => {
  fetchPlanificadores();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
