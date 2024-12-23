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
                  Planificador: {{ actividad.planificador_nombre }}<br />
                  Fecha inicio: {{ actividad.fecha_inicio }}<br />
                  Fecha fin: {{ actividad.fecha_fin }}<br />
                  Color: {{ actividad.color }}<br />
                  Estado: {{ actividad.estado_nombre }}
                </v-list-item-subtitle>
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
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Actividad</v-card-title>
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
          <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
          <v-text-field v-model="form.fecha_inicio" label="Fecha Inicio" type="date" outlined required></v-text-field>
          <v-text-field v-model="form.fecha_fin" label="Fecha Fin" type="date" outlined required></v-text-field>
          <v-text-field v-model="form.color" label="Color" outlined></v-text-field>
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
const planificadores = ref([]);
const estados = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  planificador: null,
  nombre: "",
  descripcion: "",
  fecha_inicio: "",
  fecha_fin: "",
  color: "",
  estado: null,
});

async function fetchActividades() {
  try {
    const response = await fetch("http://localhost:8000/actividades/");
    if (response.ok) {
      const data = await response.json();
      actividades.value = (Array.isArray(data) ? data : data.results || []).map((actividad) => ({
        ...actividad,
        planificador_nombre: actividad.planificador.nombre,
        estado_nombre: actividad.estado ? actividad.estado.nombre : 'Sin estado',
      }));
    } else {
      console.error("Error al obtener actividades:", response.status);
      actividades.value = [];
    }
  } catch (error) {
    console.error("Error en fetchActividades:", error);
    actividades.value = [];
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
  form.value = { id: null, planificador: null, nombre: "", descripcion: "", fecha_inicio: "", fecha_fin: "", color: "", estado: null };
  dialog.value = true;
}

function editActividad(actividad) {
  dialogMode.value = "edit";
  form.value = { ...actividad, planificador: actividad.planificador.id, estado: actividad.estado ? actividad.estado.id : null };
  dialog.value = true;
}

async function saveActividad() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/actividades/"
        : `http://localhost:8000/actividades/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
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
    const response = await fetch(`http://localhost:8000/actividades/${actividad.id}/`, {
      method: "DELETE",
    });

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
  fetchPlanificadores();
  fetchEstados();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
