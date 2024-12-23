<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Registro de Progreso</v-card-title>
          <v-card-text>
            <v-list v-if="registrosProgreso.length > 0">
              <v-list-item v-for="registro in registrosProgreso" :key="registro.id">
                <v-list-item-title>{{ registro.actividad_nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Progreso: {{ registro.porcentaje }}%<br />
                  Fecha de registro: {{ registro.fecha_registro }}
                </v-list-item-subtitle>
                <v-btn icon @click="editRegistroProgreso(registro)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteRegistroProgreso(registro)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay registros de progreso disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Registro de Progreso</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar registro de progreso -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Registro de Progreso</v-card-title>
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
          <v-text-field v-model="form.porcentaje" label="Porcentaje de Progreso" type="number" outlined required></v-text-field>
          <v-text-field v-model="form.fecha_registro" label="Fecha de Registro" type="datetime-local" outlined required></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveRegistroProgreso">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const registrosProgreso = ref([]);
const actividades = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  actividad: null,
  porcentaje: 0,
  fecha_registro: "",
});

async function fetchRegistrosProgreso() {
  try {
    const response = await fetch("http://localhost:8000/registros_progreso/");
    if (response.ok) {
      const data = await response.json();
      registrosProgreso.value = (Array.isArray(data) ? data : data.results || []).map((registro) => ({
        ...registro,
        actividad_nombre: registro.actividad.nombre,
        fecha_registro: new Date(registro.fecha_registro).toLocaleString(),
      }));
    } else {
      console.error("Error al obtener registros de progreso:", response.status);
      registrosProgreso.value = [];
    }
  } catch (error) {
    console.error("Error en fetchRegistrosProgreso:", error);
    registrosProgreso.value = [];
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
  dialogMode.value = "add";
  form.value = { id: null, actividad: null, porcentaje: 0, fecha_registro: "" };
  dialog.value = true;
}

function editRegistroProgreso(registro) {
  dialogMode.value = "edit";
  form.value = { ...registro, actividad: registro.actividad.id, porcentaje: registro.porcentaje, fecha_registro: new Date(registro.fecha_registro).toISOString().slice(0, 16) };
  dialog.value = true;
}

async function saveRegistroProgreso() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/registros_progreso/"
        : `http://localhost:8000/registros_progreso/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchRegistrosProgreso();
      dialog.value = false;
    } else {
      console.error("Error al guardar registro de progreso:", response.status);
    }
  } catch (error) {
    console.error("Error en saveRegistroProgreso:", error);
  }
}

async function deleteRegistroProgreso(registro) {
  try {
    const response = await fetch(`http://localhost:8000/registros_progreso/${registro.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchRegistrosProgreso();
    } else {
      console.error("Error al eliminar registro de progreso:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteRegistroProgreso:", error);
  }
}

onMounted(() => {
  fetchRegistrosProgreso();
  fetchActividades();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
