<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Etiquetas</v-card-title>
          <v-card-text>
            <v-list v-if="etiquetas.length > 0">
              <v-list-item v-for="etiqueta in etiquetas" :key="etiqueta.id">
                <v-list-item-title>{{ etiqueta.nombre }}</v-list-item-title>
                <v-list-item-subtitle>Usuario: {{ etiqueta.usuario_username }}</v-list-item-subtitle>
                <v-btn icon @click="editEtiqueta(etiqueta)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteEtiqueta(etiqueta)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay etiquetas disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Etiqueta</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar etiqueta -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Etiqueta</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
          <v-select
            v-model="form.usuario"
            :items="usuarios"
            item-value="id"
            item-text="username"
            label="Usuario"
            outlined
            required
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveEtiqueta">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const etiquetas = ref([]);
const usuarios = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  usuario: null,
});

async function fetchEtiquetas() {
  try {
    const response = await fetch("http://localhost:8000/etiquetas/");
    if (response.ok) {
      const data = await response.json();
      etiquetas.value = (Array.isArray(data) ? data : data.results || []).map((etiqueta) => ({
        ...etiqueta,
        usuario_username: etiqueta.usuario.username,
      }));
    } else {
      console.error("Error al obtener etiquetas:", response.status);
      etiquetas.value = [];
    }
  } catch (error) {
    console.error("Error en fetchEtiquetas:", error);
    etiquetas.value = [];
  }
}

async function fetchUsuarios() {
  try {
    const response = await fetch("http://localhost:8000/usuarios/");  // Asegúrate de que el endpoint sea correcto
    if (response.ok) {
      const data = await response.json();
      usuarios.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener usuarios:", response.status);
      usuarios.value = [];
    }
  } catch (error) {
    console.error("Error en fetchUsuarios:", error);
    usuarios.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, nombre: "", usuario: null };
  dialog.value = true;
}

function editEtiqueta(etiqueta) {
  dialogMode.value = "edit";
  form.value = { ...etiqueta, usuario: etiqueta.usuario.id };
  dialog.value = true;
}

async function saveEtiqueta() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/etiquetas/"
        : `http://localhost:8000/etiquetas/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchEtiquetas();
      dialog.value = false;
    } else {
      console.error("Error al guardar etiqueta:", response.status);
    }
  } catch (error) {
    console.error("Error en saveEtiqueta:", error);
  }
}

async function deleteEtiqueta(etiqueta) {
  try {
    const response = await fetch(`http://localhost:8000/etiquetas/${etiqueta.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchEtiquetas();
    } else {
      console.error("Error al eliminar etiqueta:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteEtiqueta:", error);
  }
}

onMounted(() => {
  fetchEtiquetas();
  fetchUsuarios();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
