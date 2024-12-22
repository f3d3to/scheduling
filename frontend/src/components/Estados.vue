<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>Gestión de Estados</v-card-title>
            <v-card-text>
              <v-list v-if="estados.length > 0">
                <v-list-item v-for="estado in estados" :key="estado.id">
                  <v-list-item-title>{{ estado.nombre }}</v-list-item-title>
                  <v-list-item-subtitle>{{ estado.descripcion }}</v-list-item-subtitle>
                  <v-chip :color="estado.color" class="ma-2">{{ estado.color }}</v-chip>
                  <v-btn icon @click="editEstado(estado)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deleteEstado(estado)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info" border="left" color="blue" dark>
                No hay estados disponibles para mostrar.
              </v-alert>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="showAddDialog">Añadir Estado</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Modal para añadir/editar estado -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Estado</v-card-title>
          <v-card-text>
            <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
            <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
            <v-text-field
              v-model="form.color"
              label="Color (Hexadecimal)"
              outlined
              required
            ></v-text-field>
            <v-text-field v-model.number="form.orden" label="Orden" type="number" outlined></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="saveEstado">Guardar</v-btn>
            <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted } from "vue";

  const estados = ref([]);
  const dialog = ref(false);
  const dialogMode = ref("add");
  const form = ref({
    id: null,
    nombre: "",
    descripcion: "",
    color: "#FFFFFF",
    orden: 0,
  });

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

  function showAddDialog() {
    dialogMode.value = "add";
    form.value = { id: null, nombre: "", descripcion: "", color: "#FFFFFF", orden: 0 };
    dialog.value = true;
  }

  function editEstado(estado) {
    dialogMode.value = "edit";
    form.value = { ...estado };
    dialog.value = true;
  }

  async function saveEstado() {
    try {
      const method = dialogMode.value === "add" ? "POST" : "PUT";
      const url =
        dialogMode.value === "add"
          ? "http://localhost:8000/estados/"
          : `http://localhost:8000/estados/${form.value.id}/`;

      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form.value),
      });

      if (response.ok) {
        fetchEstados();
        dialog.value = false;
      } else {
        console.error("Error al guardar estado:", response.status);
      }
    } catch (error) {
      console.error("Error en saveEstado:", error);
    }
  }

  async function deleteEstado(estado) {
    try {
      const response = await fetch(
        `http://localhost:8000/estados/${estado.id}/`,
        { method: "DELETE" }
      );

      if (response.ok) {
        fetchEstados();
      } else {
        console.error("Error al eliminar estado:", response.status);
      }
    } catch (error) {
      console.error("Error en deleteEstado:", error);
    }
  }

  onMounted(() => {
    fetchEstados();
  });
  </script>

  <style scoped>
  .v-chip {
    font-weight: bold;
    text-transform: capitalize;
  }
  </style>
