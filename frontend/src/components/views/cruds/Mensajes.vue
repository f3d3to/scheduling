<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Mensajes</v-card-title>
          <v-card-text>
            <v-list v-if="mensajes.length > 0">
              <v-list-item v-for="mensaje in mensajes" :key="mensaje.id">
                <v-list-item-title>Tipo: {{ mensaje.tipo }}</v-list-item-title>
                <v-list-item-subtitle>
                  Icono: {{ mensaje.icono }} - Color: <v-chip :color="mensaje.color">{{ mensaje.color }}</v-chip>
                </v-list-item-subtitle>
                <v-btn icon @click="editMensaje(mensaje)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteMensaje(mensaje)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay mensajes disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Mensaje</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar mensaje -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Mensaje</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.elemento"
            :items="elementos"
            item-value="id"
            item-text="nombre"
            label="Elemento"
            outlined
            required
          ></v-select>
          <v-text-field v-model="form.tipo" label="Tipo" outlined required></v-text-field>
          <v-text-field v-model="form.icono" label="Icono" outlined></v-text-field>
          <v-text-field v-model="form.color" label="Color (Hexadecimal)" outlined></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveMensaje">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const mensajes = ref([]);
const elementos = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  elemento: null,
  tipo: "",
  icono: "",
  color: "#FFFFFF",
});

async function fetchMensajes() {
  try {
    const response = await fetch("http://localhost:8000/mensajes/");
    if (response.ok) {
      const data = await response.json();
      mensajes.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener mensajes:", response.status);
      mensajes.value = [];
    }
  } catch (error) {
    console.error("Error en fetchMensajes:", error);
    mensajes.value = [];
  }
}

async function fetchElementos() {
  try {
    const response = await fetch("http://localhost:8000/elementos/");
    if (response.ok) {
      const data = await response.json();
      elementos.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener elementos:", response.status);
      elementos.value = [];
    }
  } catch (error) {
    console.error("Error en fetchElementos:", error);
    elementos.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, elemento: null, tipo: "", icono: "", color: "#FFFFFF" };
  dialog.value = true;
}

function editMensaje(mensaje) {
  dialogMode.value = "edit";
  form.value = { ...mensaje };
  dialog.value = true;
}

async function saveMensaje() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/mensajes/"
        : `http://localhost:8000/mensajes/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchMensajes();
      dialog.value = false;
    } else {
      console.error("Error al guardar mensaje:", response.status);
    }
  } catch (error) {
    console.error("Error en saveMensaje:", error);
  }
}

async function deleteMensaje(mensaje) {
  try {
    const response = await fetch(`http://localhost:8000/mensajes/${mensaje.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchMensajes();
    } else {
      console.error("Error al eliminar mensaje:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteMensaje:", error);
  }
}

onMounted(() => {
  fetchMensajes();
  fetchElementos();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
