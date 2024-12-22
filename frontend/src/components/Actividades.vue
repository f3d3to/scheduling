<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>Gestión de Actividades</v-card-title>
            <v-card-text>
              <v-list v-if="actividades.length > 0">
                <v-list-item v-for="actividad in actividades" :key="actividad.id">
                  <v-list-item-title>{{ actividad.nombre }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ actividad.descripcion || "Sin descripción" }}
                  </v-list-item-subtitle>
                  <v-chip color="primary" class="ma-2">{{ actividad.estado?.nombre || "Sin Estado" }}</v-chip>
                  <v-chip color="secondary" class="ma-2">{{ actividad.planificador?.nombre || "Sin Planificador" }}</v-chip>
                  <v-btn icon @click="editActividad(actividad)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deleteActividad(actividad)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info" border="left" color="blue" dark>
                No hay actividades disponibles para mostrar.
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="showAddDialog">Añadir Actividad</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Modal para añadir/editar actividad -->
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Actividad</v-card-title>
          <v-card-text>
            <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
            <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
            <v-select
              v-model="form.planificador"
              :items="planificadores"
              item-text="nombre"
              item-value="id"
              label="Planificador"
              outlined
            ></v-select>
            <v-select
              v-model="form.estado"
              :items="estados"
              item-text="nombre"
              item-value="id"
              label="Estado"
              outlined
            ></v-select>
            <v-date-picker
              v-model="form.fecha_inicio"
              label="Fecha de Inicio"
              outlined
            ></v-date-picker>
            <v-date-picker
              v-model="form.fecha_fin"
              label="Fecha de Fin"
              outlined
            ></v-date-picker>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="saveActividad">Guardar</v-btn>
            <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted } from "vue";

  const actividades = ref([]);
  const estados = ref([]);
  const planificadores = ref([]);
  const dialog = ref(false);
  const dialogMode = ref("add");
  const form = ref({
    id: null,
    nombre: "",
    descripcion: "",
    estado: null,
    planificador: null,
    fecha_inicio: null,
    fecha_fin: null,
  });

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

  async function fetchEstados() {
    try {
      const response = await fetch("http://localhost:8000/estados/");
      if (response.ok) {
        const data = await response.json();
        estados.value = Array.isArray(data) ? data : data.results || [];
      } else {
        console.error("Error al obtener estados:", response.status);
        estados.value = [];
      }
    } catch (error) {
      console.error("Error en fetchEstados:", error);
      estados.value = [];
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
    form.value = {
      id: null,
      nombre: "",
      descripcion: "",
      estado: null,
      planificador: null,
      fecha_inicio: null,
      fecha_fin: null,
    };
    dialog.value = true;
  }

  function editActividad(actividad) {
    dialogMode.value = "edit";
    form.value = {
      id: actividad.id,
      nombre: actividad.nombre,
      descripcion: actividad.descripcion,
      estado: actividad.estado?.id || null,
      planificador: actividad.planificador?.id || null,
      fecha_inicio: actividad.fecha_inicio,
      fecha_fin: actividad.fecha_fin,
    };
    dialog.value = true;
  }

  async function saveActividad() {
    try {
      const method = dialogMode.value === "add" ? "POST" : "PUT";
      const url =
        dialogMode.value === "add"
          ? "http://localhost:8000/actividades/"
          : `http://localhost:8000/actividades/${form.value.id}/`;

      const payload = {
        nombre: form.value.nombre,
        descripcion: form.value.descripcion,
        estado: form.value.estado,
        planificador: form.value.planificador,
        fecha_inicio: form.value.fecha_inicio,
        fecha_fin: form.value.fecha_fin,
      };

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        fetchActividades();
        dialog.value = false;
      } else {
        console.error("Error al guardar actividad:", response.status);
      }
    } catch (error) {
      console.error("Error en saveActividad:", error);
    }
  }

  async function deleteActividad(actividad) {
    try {
      const response = await fetch(
        `http://localhost:8000/actividades/${actividad.id}/`,
        { method: "DELETE" }
      );

      if (response.ok) {
        fetchActividades();
      } else {
        console.error("Error al eliminar actividad:", response.status);
      }
    } catch (error) {
      console.error("Error en deleteActividad:", error);
    }
  }

  onMounted(() => {
    fetchActividades();
    fetchEstados();
    fetchPlanificadores();
  });
  </script>

  <style scoped>
  .v-chip {
    font-weight: bold;
    text-transform: capitalize;
  }
  </style>
