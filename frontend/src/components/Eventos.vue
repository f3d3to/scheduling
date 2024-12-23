<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Eventos</v-card-title>
          <v-card-text>
            <v-list v-if="eventos.length > 0">
              <v-list-item v-for="evento in eventos" :key="evento.id">
                <v-list-item-title>{{ evento.nombre }}</v-list-item-title>
                <v-list-item-subtitle>
                  Fecha y hora: {{ evento.fecha_hora }}<br />
                  Descripción: {{ evento.descripcion }}<br />
                  Usuario: {{ evento.usuario_username }}
                </v-list-item-subtitle>
                <v-btn icon @click="editEvento(evento)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteEvento(evento)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay eventos disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Evento</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar evento -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Evento</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.nombre" label="Nombre del Evento" outlined required></v-text-field>
          <v-textarea v-model="form.descripcion" label="Descripción" outlined></v-textarea>
          <v-text-field v-model="form.fecha_hora" label="Fecha y Hora" type="datetime-local" outlined required></v-text-field>
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
          <v-btn color="success" @click="saveEvento">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const eventos = ref([]);
const usuarios = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  nombre: "",
  descripcion: "",
  fecha_hora: "",
  usuario: null,
});

async function fetchEventos() {
  try {
    const response = await fetch("http://localhost:8000/eventos/");
    if (response.ok) {
      const data = await response.json();
      eventos.value = (Array.isArray(data) ? data : data.results || []).map((evento) => ({
        ...evento,
        usuario_username: evento.usuario.username,
      }));
    } else {
      console.error("Error al obtener eventos:", response.status);
      eventos.value = [];
    }
  } catch (error) {
    console.error("Error en fetchEventos:", error);
    eventos.value = [];
  }
}

async function fetchUsuarios() {
  try {
    const response = await fetch("http://localhost:8000/usuarios/");
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
  form.value = { id: null, nombre: "", descripcion: "", fecha_hora: "", usuario: null };
  dialog.value = true;
}

function editEvento(evento) {
  dialogMode.value = "edit";
  form.value = { ...evento, usuario: evento.usuario.id };
  dialog.value = true;
}

async function saveEvento() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/eventos/"
        : `http://localhost:8000/eventos/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchEventos();
      dialog.value = false;
    } else {
      console.error("Error al guardar evento:", response.status);
    }
  } catch (error) {
    console.error("Error en saveEvento:", error);
  }
}

async function deleteEvento(evento) {
  try {
    const response = await fetch(`http://localhost:8000/eventos/${evento.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchEventos();
    } else {
      console.error("Error al eliminar evento:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteEvento:", error);
  }
}

onMounted(() => {
  fetchEventos();
  fetchUsuarios();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
