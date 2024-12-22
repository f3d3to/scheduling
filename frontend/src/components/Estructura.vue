<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>Gestión de Estructuras de Planificador</v-card-title>
            <v-card-text>
              <v-list v-if="estructuras.length > 0">
                <v-list-item v-for="estructura in estructuras" :key="estructura.id">
                  <v-list-item-title>{{ estructura.nombre }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ estructura.descripcion || "Sin descripción" }}
                  </v-list-item-subtitle>
                  <v-btn icon @click="editEstructura(estructura)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deleteEstructura(estructura)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info" border="left" color="blue" dark>
                No hay estructuras disponibles para mostrar.
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="showAddDialog">Añadir Estructura</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Modal para añadir/editar estructura -->
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Estructura</v-card-title>
          <v-card-text>
            <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
            <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
            <v-textarea
              v-model="form.configuracion"
              label="Configuración (JSON)"
              outlined
              rows="6"
            ></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="saveEstructura">Guardar</v-btn>
            <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted } from "vue";

  const estructuras = ref([]);
  const dialog = ref(false);
  const dialogMode = ref("add");
  const form = ref({
    id: null,
    nombre: "",
    descripcion: "",
    configuracion: "",
  });

  async function fetchEstructuras() {
    try {
      const response = await fetch("http://localhost:8000/estructuras/");
      if (response.ok) {
        const data = await response.json();
        estructuras.value = Array.isArray(data) ? data : data.results || [];
      } else {
        console.error("Error al obtener estructuras:", response.status);
        estructuras.value = [];
      }
    } catch (error) {
      console.error("Error en fetchEstructuras:", error);
      estructuras.value = [];
    }
  }

  function showAddDialog() {
    dialogMode.value = "add";
    form.value = { id: null, nombre: "", descripcion: "", configuracion: "" };
    dialog.value = true;
  }

  function editEstructura(estructura) {
    dialogMode.value = "edit";
    form.value = {
      id: estructura.id,
      nombre: estructura.nombre,
      descripcion: estructura.descripcion,
      configuracion: JSON.stringify(estructura.configuracion, null, 2),
    };
    dialog.value = true;
  }

  async function saveEstructura() {
    try {
      const method = dialogMode.value === "add" ? "POST" : "PUT";
      const url =
        dialogMode.value === "add"
          ? "http://localhost:8000/estructuras/"
          : `http://localhost:8000/estructuras/${form.value.id}/`;

      const payload = {
        nombre: form.value.nombre,
        descripcion: form.value.descripcion,
        configuracion: JSON.parse(form.value.configuracion || "{}"),
      };

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        fetchEstructuras();
        dialog.value = false;
      } else {
        console.error("Error al guardar estructura:", response.status);
      }
    } catch (error) {
      console.error("Error en saveEstructura:", error);
    }
  }

  async function deleteEstructura(estructura) {
    try {
      const response = await fetch(
        `http://localhost:8000/estructuras/${estructura.id}/`,
        { method: "DELETE" }
      );

      if (response.ok) {
        fetchEstructuras();
      } else {
        console.error("Error al eliminar estructura:", response.status);
      }
    } catch (error) {
      console.error("Error en deleteEstructura:", error);
    }
  }

  onMounted(() => {
    fetchEstructuras();
  });
  </script>

  <style scoped>
  .v-chip {
    font-weight: bold;
    text-transform: capitalize;
  }
  </style>
