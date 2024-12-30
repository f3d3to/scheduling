<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Eventos Asociados</v-card-title>
          <v-card-text>
            <v-list v-if="eventosAsociados.length > 0">
              <v-list-item v-for="eventoAsociado in eventosAsociados" :key="eventoAsociado.id">
                <v-list-item-title>{{ eventoAsociado.evento_nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Objeto: {{ eventoAsociado.objecto_nombre }}<br />
                  Tipo de objeto: {{ eventoAsociado.content_type }}
                </v-list-item-subtitle>
                <v-btn icon @click="editEventoAsociado(eventoAsociado)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteEventoAsociado(eventoAsociado)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay eventos asociados disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Evento Asociado</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar evento asociado -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Evento Asociado</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.evento"
            :items="eventos"
            item-value="id"
            item-text="nombre"
            label="Evento"
            outlined
            required
          ></v-select>
          <v-select
            v-model="form.content_type"
            :items="contentTypes"
            label="Tipo de Objeto"
            outlined
            required
          ></v-select>
          <v-select
            v-model="form.object_id"
            :items="objects"
            item-value="id"
            item-text="nombre"
            label="Objeto"
            outlined
            required
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveEventoAsociado">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const eventosAsociados = ref([]);
const eventos = ref([]);
const contentTypes = ref(["Elemento", "Actividad", "Tarea", "Planificador"]);
const objects = ref([]); // Aquí puedes definir los objetos según lo que necesites
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  evento: null,
  content_type: "Elemento", // Cambia según el tipo que quieras por defecto
  object_id: null,
});

async function fetchEventosAsociados() {
  try {
    const response = await fetch("http://localhost:8000/eventos-asociados/");
    if (response.ok) {
      const data = await response.json();
      eventosAsociados.value = (Array.isArray(data) ? data : data.results || []).map((eventoAsociado) => ({
        ...eventoAsociado,
        evento_nombre: eventoAsociado.evento.nombre,
        objecto_nombre: eventoAsociado.content_object ? eventoAsociado.content_object.nombre : "Sin objeto",
        content_type: eventoAsociado.content_type.model,
      }));
    } else {
      console.error("Error al obtener eventos asociados:", response.status);
      eventosAsociados.value = [];
    }
  } catch (error) {
    console.error("Error en fetchEventosAsociados:", error);
    eventosAsociados.value = [];
  }
}

async function fetchEventos() {
  try {
    const response = await fetch("http://localhost:8000/eventos/");
    if (response.ok) {
      const data = await response.json();
      eventos.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener eventos:", response.status);
      eventos.value = [];
    }
  } catch (error) {
    console.error("Error en fetchEventos:", error);
    eventos.value = [];
  }
}

async function fetchObjects() {
  try {
    const response = await fetch("http://localhost:8000/elementos/");  // Ajusta el endpoint según los objetos que quieras asociar
    if (response.ok) {
      const data = await response.json();
      objects.value = Array.isArray(data) ? data : data.results || [];
    } else {
      console.error("Error al obtener objetos:", response.status);
      objects.value = [];
    }
  } catch (error) {
    console.error("Error en fetchObjects:", error);
    objects.value = [];
  }
}

function showAddDialog() {
  dialogMode.value = "add";
  form.value = { id: null, evento: null, content_type: "Elemento", object_id: null };
  dialog.value = true;
}

function editEventoAsociado(eventoAsociado) {
  dialogMode.value = "edit";
  form.value = {
    ...eventoAsociado,
    evento: eventoAsociado.evento.id,
    content_type: eventoAsociado.content_type.model,
    object_id: eventoAsociado.object_id
  };
  dialog.value = true;
}

async function saveEventoAsociado() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/eventos-asociados/"
        : `http://localhost:8000/eventos-asociados/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchEventosAsociados();
      dialog.value = false;
    } else {
      console.error("Error al guardar evento asociado:", response.status);
    }
  } catch (error) {
    console.error("Error en saveEventoAsociado:", error);
  }
}

async function deleteEventoAsociado(eventoAsociado) {
  try {
    const response = await fetch(`http://localhost:8000/eventos-asociados/${eventoAsociado.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchEventosAsociados();
    } else {
      console.error("Error al eliminar evento asociado:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteEventoAsociado:", error);
  }
}

onMounted(() => {
  fetchEventosAsociados();
  fetchEventos();
  fetchObjects();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
