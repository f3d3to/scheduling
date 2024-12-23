<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>Gestión de Celdas</v-card-title>
            <v-card-text>
              <v-list v-if="celdas.length > 0">
                <v-list-item v-for="celda in celdas" :key="celda.id">
                  <v-list-item-title>{{ celda.planificador_nombre }}</v-list-item-title>
                  <v-list-item-subtitle>{{ celda.contenido }}</v-list-item-subtitle>
                  <v-btn icon @click="editCelda(celda)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deleteCelda(celda)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info" border="left" color="blue" dark>
                No hay celdas disponibles para mostrar.
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="showAddDialog">Añadir Celda</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Modal para añadir/editar celda -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Celda</v-card-title>
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
            <v-text-field v-model="form.contenido" label="Contenido" outlined required></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="saveCelda">Guardar</v-btn>
            <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted } from "vue";

  const celdas = ref([]);
  const planificadores = ref([]);
  const dialog = ref(false);
  const dialogMode = ref("add");
  const form = ref({
    id: null,
    planificador: null,
    contenido: "",
  });

  async function fetchCeldas() {
    try {
      const response = await fetch("http://localhost:8000/celdas/");
      if (response.ok) {
        const data = await response.json();
        celdas.value = (Array.isArray(data) ? data : data.results || []).map((celda) => ({
          ...celda,
          planificador_nombre: celda.planificador.nombre,
        }));
      } else {
        console.error("Error al obtener celdas:", response.status);
        celdas.value = [];
      }
    } catch (error) {
      console.error("Error en fetchCeldas:", error);
      celdas.value = [];
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
    form.value = { id: null, planificador: null, contenido: "" };
    dialog.value = true;
  }

  function editCelda(celda) {
    dialogMode.value = "edit";
    form.value = { id: celda.id, planificador: celda.planificador, contenido: celda.contenido };
    dialog.value = true;
  }

  async function saveCelda() {
    try {
      const method = dialogMode.value === "add" ? "POST" : "PUT";
      const url =
        dialogMode.value === "add"
          ? "http://localhost:8000/celdas/"
          : `http://localhost:8000/celdas/${form.value.id}/`;

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form.value),
      });

      if (response.ok) {
        fetchCeldas();
        dialog.value = false;
      } else {
        console.error("Error al guardar celda:", response.status);
      }
    } catch (error) {
      console.error("Error en saveCelda:", error);
    }
  }

  async function deleteCelda(celda) {
    try {
      const response = await fetch(`http://localhost:8000/celdas/${celda.id}/`, {
        method: "DELETE",
      });

      if (response.ok) {
        fetchCeldas();
      } else {
        console.error("Error al eliminar celda:", response.status);
      }
    } catch (error) {
      console.error("Error en deleteCelda:", error);
    }
  }

  onMounted(() => {
    fetchCeldas();
    fetchPlanificadores();
  });
  </script>

  <style scoped>
  .v-btn {
    margin-left: 8px;
  }
  </style>
