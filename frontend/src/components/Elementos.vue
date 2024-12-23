<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Elementos</v-card-title>
          <v-card-text>
            <v-list v-if="elementos.length > 0">
              <v-list-item v-for="elemento in elementos" :key="elemento.id">
                <v-list-item-title>{{ elemento.nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Celda: {{ elemento.celda_nombre }}<br />
                  Descripción: {{ elemento.descripcion }}<br />
                  Tipo de contenido: {{ elemento.content_type }}
                </v-list-item-subtitle>
                <v-btn icon @click="editElemento(elemento)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteElemento(elemento)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay elementos disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Elemento</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar elemento -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Elemento</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.nombre" label="Nombre del Elemento" outlined required></v-text-field>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
          <v-select
            v-model="form.celda"
            :items="celdas"
            item-value="id"
            item-text="contenido"
            label="Celda"
            outlined
            required
          ></v-select>
          <v-select
            v-model="form.content_type"
            :items="contentTypes"
            label="Tipo de Contenido"
            outlined
            required
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveElemento">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const elementos = ref([]);
const celdas = ref([]);
const contentTypes = ref(["Actividad", "Tarea", "Planificador", "Elemento"]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  descripcion: "",
  celda: null,
  content_type: "Elemento", // Cambiar según lo que se necesite por defecto
});

async function fetchElementos() {
  try {
    const response = await fetch("http://localhost:8000/elementos/");
    if (response.ok) {
      const data = await response.json();
      elementos.value = (Array.isArray(data) ? data : data.results || []).map((elemento) => ({
        ...elemento,
        celda_nombre: elemento.celda ? elemento.celda.contenido : "Sin celda",
        content_type: elemento.content_type.model,
      }));
    } else {
      console.error("Error al obtener elementos:", response.status);
      elementos.value = [];
    }
  } catch (error) {
    console.error("Error en fetchElementos:", error);
    elementos.value = [];
  }
}

async function fetchCeldas() {
  try {
    const response = await fetch("http://localhost:8000/celdas/");
    if (response.ok) {
      const data = await response.json();
      celdas.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener celdas:", response.status);
      celdas.value = [];
    }
  } catch (error) {
    console.error("Error en fetchCeldas:", error);
    celdas.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, nombre: "", descripcion: "", celda: null, content_type: "Elemento" };
  dialog.value = true;
}

function editElemento(elemento) {
  dialogMode.value = "edit";
  form.value = {
    ...elemento,
    celda: elemento.celda ? elemento.celda.id : null,
    content_type: elemento.content_type.model
  };
  dialog.value = true;
}

async function saveElemento() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/elementos/"
        : `http://localhost:8000/elementos/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchElementos();
      dialog.value = false;
    } else {
      console.error("Error al guardar elemento:", response.status);
    }
  } catch (error) {
    console.error("Error en saveElemento:", error);
  }
}

async function deleteElemento(elemento) {
  try {
    const response = await fetch(`http://localhost:8000/elementos/${elemento.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchElementos();
    } else {
      console.error("Error al eliminar elemento:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteElemento:", error);
  }
}

onMounted(() => {
  fetchElementos();
  fetchCeldas();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
