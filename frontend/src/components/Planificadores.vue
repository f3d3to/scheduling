<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Planificadores</v-card-title>
          <v-card-text>
            <v-list v-if="planificadores.length > 0">
              <v-list-item v-for="planificador in planificadores" :key="planificador.id">
                <v-list-item-title>{{ planificador.nombre }}</v-list-item-title>
                <v-list-item-subtitle>{{ planificador.descripcion }}</v-list-item-subtitle>
                <v-chip color="primary" class="ma-2">{{ planificador.tipo?.nombre || 'Sin Tipo' }}</v-chip>
                <v-chip color="secondary" class="ma-2">{{ planificador.estructura?.nombre || 'Sin Estructura' }}</v-chip>
                <v-btn icon @click="editPlanificador(planificador)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deletePlanificador(planificador)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay planificadores disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Planificador</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar planificador -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Planificador</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
          <v-select
            v-model="form.tipo"
            :items="tiposPlanificador"
            item-text="nombre"
            item-value="id"
            label="Tipo de Planificador"
            outlined
          ></v-select>
          <v-select
            v-model="form.estructura"
            :items="estructurasPlanificador"
            item-text="nombre"
            item-value="id"
            label="Estructura de Planificador"
            outlined
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="savePlanificador">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const planificadores = ref([]);
const tiposPlanificador = ref([]);
const estructurasPlanificador = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  descripcion: "",
  tipo: null,
  estructura: null,
});

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

async function fetchTiposPlanificador() {
  try {
    const response = await fetch("http://localhost:8000/tipos-planificador/");
    if (response.ok) {
      const data = await response.json();
      tiposPlanificador.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener tipos de planificador:", response.status);
      tiposPlanificador.value = [];
    }
  } catch (error) {
    console.error("Error en fetchTiposPlanificador:", error);
    tiposPlanificador.value = [];
  }
}

async function fetchEstructurasPlanificador() {
  try {
    const response = await fetch("http://localhost:8000/estructuras/");
    if (response.ok) {
      const data = await response.json();
      estructurasPlanificador.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener estructuras de planificador:", response.status);
      estructurasPlanificador.value = [];
    }
  } catch (error) {
    console.error("Error en fetchEstructurasPlanificador:", error);
    estructurasPlanificador.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, nombre: "", descripcion: "", tipo: null, estructura: null };
  dialog.value = true;
}

function editPlanificador(planificador) {
  dialogMode.value = "edit";
  form.value = {
    id: planificador.id,
    nombre: planificador.nombre,
    descripcion: planificador.descripcion,
    tipo: planificador.tipo?.id || null,
    estructura: planificador.estructura?.id || null,
  };
  dialog.value = true;
}

async function savePlanificador() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/planificadores/"
        : `http://localhost:8000/planificadores/${form.value.id}/`;

    const payload = {
      nombre: form.value.nombre,
      descripcion: form.value.descripcion,
      tipo: form.value.tipo,
      estructura: form.value.estructura,
    };

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      fetchPlanificadores();
      dialog.value = false;
    } else {
      console.error("Error al guardar planificador:", response.status);
    }
  } catch (error) {
    console.error("Error en savePlanificador:", error);
  }
}

async function deletePlanificador(planificador) {
  try {
    const response = await fetch(
      `http://localhost:8000/planificadores/${planificador.id}/`,
      { method: "DELETE" }
    );

    if (response.ok) {
      fetchPlanificadores();
    } else {
      console.error("Error al eliminar planificador:", response.status);
    }
  } catch (error) {
    console.error("Error en deletePlanificador:", error);
  }
}

onMounted(() => {
  fetchPlanificadores();
  fetchTiposPlanificador();
  fetchEstructurasPlanificador();
});
</script>

<style scoped>
.v-chip {
  font-weight: bold;
  text-transform: capitalize;
}
</style>
