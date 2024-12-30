<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Tareas</v-card-title>
          <v-card-text>
            <v-list v-if="tareas.length > 0">
              <v-list-item v-for="tarea in tareas" :key="tarea.id">
                <v-list-item-title>{{ tarea.nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Actividad: {{ tarea.actividad_nombre }}<br />
                  Fecha límite: {{ tarea.fecha_limite }}<br />
                  Completada: {{ tarea.esta_realizada ? "Sí" : "No" }}<br />
                  Estado: {{ tarea.estado_nombre }}
                </v-list-item-subtitle>
                <v-btn icon @click="editTarea(tarea)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteTarea(tarea)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay tareas disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Tarea</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar tarea -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Tarea</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.actividad"
            :items="actividades"
            item-value="id"
            item-text="nombre"
            label="Actividad"
            outlined
            required
          ></v-select>
          <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
          <v-text-field v-model="form.fecha_limite" label="Fecha Límite" type="date" outlined required></v-text-field>
          <v-checkbox v-model="form.esta_realizada" label="Completada"></v-checkbox>
          <v-select
            v-model="form.estado"
            :items="estados"
            item-value="id"
            item-text="nombre"
            label="Estado"
            outlined
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveTarea">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const tareas = ref([]);
const actividades = ref([]);
const estados = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  actividad: null,
  nombre: "",
  descripcion: "",
  fecha_limite: "",
  esta_realizada: false,
  estado: null,
});

async function fetchTareas() {
  try {
    const response = await fetch("http://localhost:8000/tareas/");
    if (response.ok) {
      const data = await response.json();
      tareas.value = (Array.isArray(data) ? data : data.results || []).map((tarea) => ({
        ...tarea,
        actividad_nombre: tarea.actividad.nombre,
        estado_nombre: tarea.estado ? tarea.estado.nombre : 'Sin estado',
      }));
    } else {
      console.error("Error al obtener tareas:", response.status);
      tareas.value = [];
    }
  } catch (error) {
    console.error("Error en fetchTareas:", error);
    tareas.value = [];
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
  form.value = { id: null, actividad: null, nombre: "", descripcion: "", fecha_limite: "", esta_realizada: false, estado: null };
  dialog.value = true;
}

function editTarea(tarea) {
  dialogMode.value = "edit";
  form.value = { ...tarea, actividad: tarea.actividad.id, estado: tarea.estado ? tarea.estado.id : null };
  dialog.value = true;
}

async function saveTarea() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/tareas/"
        : `http://localhost:8000/tareas/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchTareas();
      dialog.value = false;
    } else {
      console.error("Error al guardar tarea:", response.status);
    }
  } catch (error) {
    console.error("Error en saveTarea:", error);
  }
}

async function deleteTarea(tarea) {
  try {
    const response = await fetch(`http://localhost:8000/tareas/${tarea.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchTareas();
    } else {
      console.error("Error al eliminar tarea:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteTarea:", error);
  }
}

onMounted(() => {
  fetchTareas();
  fetchActividades();
  fetchEstados();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
