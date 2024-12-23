<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Elementos Recurrentes</v-card-title>
          <v-card-text>
            <v-list v-if="recurrentes.length > 0">
              <v-list-item v-for="recurrente in recurrentes" :key="recurrente.id">
                <v-list-item-subtitle>
                  Frecuencia: {{ recurrente.frecuencia }}<br />
                  Próxima fecha: {{ recurrente.proxima_fecha }}<br />
                </v-list-item-subtitle>
                <v-btn icon @click="editRecurrente(recurrente)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteRecurrente(recurrente)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay elementos recurrentes disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Elemento Recurrente</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar recurrente -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Elemento Recurrente</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.frecuencia"
            :items="frecuencias"
            label="Frecuencia"
            outlined
            required
          ></v-select>
          <v-text-field v-model="form.proxima_fecha" label="Próxima Fecha" type="date" outlined required></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveRecurrente">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const recurrentes = ref([]);
const frecuencias = ref(["Diaria", "Semanal", "Mensual"]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  frecuencia: "Diaria",
  proxima_fecha: "",
});

async function fetchRecurrentes() {
  try {
    const response = await fetch("http://localhost:8000/recurrentes/");
    if (response.ok) {
      const data = await response.json();
      recurrentes.value = (Array.isArray(data) ? data : data.results || []).map((recurrente) => ({
        ...recurrente,
      }));
    } else {
      console.error("Error al obtener recurrentes:", response.status);
      recurrentes.value = [];
    }
  } catch (error) {
    console.error("Error en fetchRecurrentes:", error);
    recurrentes.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, frecuencia: "Diaria", proxima_fecha: "" };
  dialog.value = true;
}

function editRecurrente(recurrente) {
  dialogMode.value = "edit";
  form.value = { ...recurrente };
  dialog.value = true;
}

async function saveRecurrente() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/recurrentes/"
        : `http://localhost:8000/recurrentes/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchRecurrentes();
      dialog.value = false;
    } else {
      console.error("Error al guardar recurrente:", response.status);
    }
  } catch (error) {
    console.error("Error en saveRecurrente:", error);
  }
}

async function deleteRecurrente(recurrente) {
  try {
    const response = await fetch(`http://localhost:8000/recurrentes/${recurrente.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchRecurrentes();
    } else {
      console.error("Error al eliminar recurrente:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteRecurrente:", error);
  }
}

onMounted(() => {
  fetchRecurrentes();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
