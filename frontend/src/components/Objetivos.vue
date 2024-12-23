<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Objetivos</v-card-title>
          <v-card-text>
            <v-list v-if="objetivos.length > 0">
              <v-list-item v-for="objetivo in objetivos" :key="objetivo.id">
                <v-list-item-title>{{ objetivo.descripcion }}</v-list-item-title>
                <v-list-item-subtitle>
                  Planificador: {{ objetivo.planificador_nombre }}<br />
                  Fecha objetivo: {{ objetivo.fecha_objetivo }}<br />
                  Completado: {{ objetivo.completado ? "Sí" : "No" }}
                </v-list-item-subtitle>
                <v-btn icon @click="editObjetivo(objetivo)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteObjetivo(objetivo)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay objetivos disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Objetivo</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar objetivo -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Objetivo</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.planificador"
            :items="planificadores"
            item-value="id"
            item-text="nombre"
            label="Planificador"
            outlined
            required
          ></v-select>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined required></v-textarea>
          <v-text-field v-model="form.fecha_objetivo" label="Fecha Objetivo" type="date" outlined required></v-text-field>
          <v-checkbox v-model="form.completado" label="Completado"></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveObjetivo">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const objetivos = ref([]);
const planificadores = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  planificador: null,
  descripcion: "",
  fecha_objetivo: "",
  completado: false,
});

async function fetchObjetivos() {
  try {
    const response = await fetch("http://localhost:8000/objetivos/");
    if (response.ok) {
      const data = await response.json();
      objetivos.value = (Array.isArray(data) ? data : data.results || []).map((objetivo) => ({
        ...objetivo,
        planificador_nombre: objetivo.planificador.nombre,
      }));
    } else {
      console.error("Error al obtener objetivos:", response.status);
      objetivos.value = [];
    }
  } catch (error) {
    console.error("Error en fetchObjetivos:", error);
    objetivos.value = [];
  }
}

async function fetchPlanificadores() {
  try {
    const response = await fetch("http://localhost:8000/planificadores/");
    if (response.ok) {
      const data = await response.json();
      planificadores.value = Array.isArray(data) ? data : data.results || [];
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
  form.value = { id: null, planificador: null, descripcion: "", fecha_objetivo: "", completado: false };
  dialog.value = true;
}

function editObjetivo(objetivo) {
  dialogMode.value = "edit";
  form.value = { ...objetivo, planificador: objetivo.planificador.id };
  dialog.value = true;
}

async function saveObjetivo() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/objetivos/"
        : `http://localhost:8000/objetivos/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchObjetivos();
      dialog.value = false;
    } else {
      console.error("Error al guardar objetivo:", response.status);
    }
  } catch (error) {
    console.error("Error en saveObjetivo:", error);
  }
}

async function deleteObjetivo(objetivo) {
  try {
    const response = await fetch(`http://localhost:8000/objetivos/${objetivo.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchObjetivos();
    } else {
      console.error("Error al eliminar objetivo:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteObjetivo:", error);
  }
}

onMounted(() => {
  fetchObjetivos();
  fetchPlanificadores();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
