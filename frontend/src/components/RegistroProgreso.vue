<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>Gestión de Registro de Progresos</v-card-title>
            <v-card-text>
              <v-list v-if="registros.length > 0">
                <v-list-item v-for="registro in registros" :key="registro.id">
                  <v-list-item-title>
                    {{ registro.actividad?.nombre || "Sin Actividad" }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Progreso: {{ registro.porcentaje }}%
                  </v-list-item-subtitle>
                  <v-list-item-subtitle>
                    Fecha: {{ registro.fecha_registro }}
                  </v-list-item-subtitle>
                  <v-btn icon @click="deleteRegistro(registro)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info" border="left" color="blue" dark>
                No hay registros de progreso disponibles para mostrar.
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="showAddDialog">Añadir Registro</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Modal para añadir registro -->
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>Añadir Registro de Progreso</v-card-title>
          <v-card-text>
            <v-select
              v-model="form.actividad"
              :items="actividades"
              item-text="nombre"
              item-value="id"
              label="Actividad"
              outlined
              required
            ></v-select>
            <v-text-field
              v-model.number="form.porcentaje"
              label="Porcentaje de Progreso"
              type="number"
              outlined
              required
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="saveRegistro">Guardar</v-btn>
            <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted } from "vue";

  const registros = ref([]);
  const actividades = ref([]);
  const dialog = ref(false);
  const form = ref({
    actividad: null,
    porcentaje: 0,
  });

  async function fetchRegistros() {
    try {
      const response = await fetch("http://localhost:8000/registros-progreso/");
      if (response.ok) {
        const data = await response.json();
        registros.value = Array.isArray(data) ? data : data.results || [];
      } else {
        console.error("Error al obtener registros de progreso:", response.status);
        registros.value = [];
      }
    } catch (error) {
      console.error("Error en fetchRegistros:", error);
      registros.value = [];
    }
  }

  async function fetchActividades() {
    try {
      const response = await fetch("http://localhost:8000/actividades/");
      if (response.ok) {
        const data = await response.json();
        actividades.value = Array.isArray(data) ? data : data.results || [];
      } else {
        console.error("Error al obtener actividades:", response.status);
        actividades.value = [];
      }
    } catch (error) {
      console.error("Error en fetchActividades:", error);
      actividades.value = [];
    }
  }

  function showAddDialog() {
    form.value = {
      actividad: null,
      porcentaje: 0,
    };
    dialog.value = true;
  }

  async function saveRegistro() {
    try {
      const response = await fetch("http://localhost:8000/registros-progreso/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form.value),
      });

      if (response.ok) {
        fetchRegistros();
        dialog.value = false;
      } else {
        console.error("Error al guardar registro de progreso:", response.status);
      }
    } catch (error) {
      console.error("Error en saveRegistro:", error);
    }
  }

  async function deleteRegistro(registro) {
    try {
      const response = await fetch(
        `http://localhost:8000/registros-progreso/${registro.id}/`,
        { method: "DELETE" }
      );

      if (response.ok) {
        fetchRegistros();
      } else {
        console.error("Error al eliminar registro de progreso:", response.status);
      }
    } catch (error) {
      console.error("Error en deleteRegistro:", error);
    }
  }

  onMounted(() => {
    fetchRegistros();
    fetchActividades();
  });
  </script>

  <style scoped>
  .v-chip {
    font-weight: bold;
    text-transform: capitalize;
  }
  </style>
