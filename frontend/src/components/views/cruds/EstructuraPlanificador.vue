<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Estructuras de Planificador</v-card-title>
          <v-card-text>
            <v-list v-if="estructurasPlanificador.length > 0">
              <v-list-item v-for="estructura in estructurasPlanificador" :key="estructura.id">
                <v-list-item-title>{{ estructura.nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Filas: {{ estructura.filas }}, Columnas: {{ estructura.columnas }}
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
              No hay estructuras de planificador disponibles para mostrar.
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
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Estructura de Planificador</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="form.nombre" label="Nombre" outlined required></v-text-field>
            <v-text-field
              v-model.number="form.filas"
              label="Filas"
              outlined
              required
              type="number"
              min="1"
            ></v-text-field>
            <v-text-field
              v-model.number="form.columnas"
              label="Columnas"
              outlined
              required
              type="number"
              min="1"
            ></v-text-field>
            <v-text-field
              v-model.number="form.ancho_columna"
              label="Ancho de la Columna (px)"
              outlined
              required
              type="number"
              min="10"
            ></v-text-field>
            <v-textarea
              v-model="form.tabla"
              label="Estructura de la Tabla (JSON)"
              outlined
              required
              rows="10"
              :error="jsonError"
              hint="Debe ser un JSON válido."
            ></v-textarea>
          </v-form>
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

const estructurasPlanificador = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  filas: 1,
  columnas: 1,
  ancho_columna: 100,
  tabla: "{}",
});
const jsonError = ref(false);

async function fetchEstructuras() {
  try {
    const response = await fetch("http://localhost:8000/estructuras-planificador/");
    if (response.ok) {
      const data = await response.json();
      estructurasPlanificador.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener estructuras de planificador:", response.status);
    }
  } catch (error) {
    console.error("Error en fetchEstructuras:", error);
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, nombre: "", filas: 1, columnas: 1, ancho_columna: 100, tabla: "{}" };
  dialog.value = true;
}

function editEstructura(estructura) {
  dialogMode.value = "edit";
  form.value = {
    id: estructura.id,
    nombre: estructura.nombre,
    filas: estructura.filas,
    columnas: estructura.columnas,
    ancho_columna: estructura.ancho_columna,
    tabla: JSON.stringify(estructura.tabla, null, 2),
  };
  dialog.value = true;
}

async function saveEstructura() {
  try {
    jsonError.value = false;

    // Validar JSON
    let tabla;
    try {
      tabla = JSON.parse(form.value.tabla);
    } catch (e) {
      jsonError.value = true;
      console.error("Error en el formato JSON de la tabla:", e);
      return;
    }

    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/estructuras-planificador/"
        : `http://localhost:8000/estructuras-planificador/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre: form.value.nombre,
        filas: form.value.filas,
        columnas: form.value.columnas,
        ancho_columna: form.value.ancho_columna,
        tabla,
      }),
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
    const response = await fetch(`http://localhost:8000/estructuras-planificador/${estructura.id}/`, {
      method: "DELETE",
    });

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
.v-btn {
  margin-left: 8px;
}
</style>
