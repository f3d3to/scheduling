<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Gestión de Comentarios</v-card-title>
          <v-card-text>
            <v-list v-if="comentarios.length > 0">
              <v-list-item v-for="comentario in comentarios" :key="comentario.id">
                <v-list-item-title>{{ comentario.contenido }}</v-list-item-title>
                <v-list-item-subtitle>
                  Usuario: {{ comentario.usuario_username }}<br />
                  Fecha: {{ comentario.fecha_creacion }}<br />
                </v-list-item-subtitle>
                <v-btn icon @click="editComentario(comentario)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteComentario(comentario)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" border="left" color="blue" dark>
              No hay comentarios disponibles para mostrar.
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="showAddDialog">Añadir Comentario</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal para añadir/editar comentario -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ dialogMode === 'add' ? 'Añadir' : 'Editar' }} Comentario</v-card-title>
        <v-card-text>
          <v-select
            v-model="form.usuario"
            :items="usuarios"
            item-value="id"
            item-text="username"
            label="Usuario"
            outlined
            required
          ></v-select>
          <v-textarea v-model="form.contenido" label="Contenido" outlined required></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn color="success" @click="saveComentario">Guardar</v-btn>
          <v-btn color="error" text @click="dialog = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";

const comentarios = ref([]);
const usuarios = ref([]);
const dialog = ref(false);
const dialogMode = ref("add");
const form = ref({
  id: null,
  contenido: "",
  usuario: null,
});

async function fetchComentarios() {
  try {
    const response = await fetch("http://localhost:8000/comentarios/");
    if (response.ok) {
      const data = await response.json();
      comentarios.value = (Array.isArray(data) ? data : data.results || []).map((comentario) => ({
        ...comentario,
        usuario_username: comentario.usuario.username,
      }));
    } else {
      console.error("Error al obtener comentarios:", response.status);
      comentarios.value = [];
    }
  } catch (error) {
    console.error("Error en fetchComentarios:", error);
    comentarios.value = [];
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
  form.value = { id: null, contenido: "", usuario: null };
  dialog.value = true;
}

function editComentario(comentario) {
  dialogMode.value = "edit";
  form.value = { ...comentario, usuario: comentario.usuario.id };
  dialog.value = true;
}

async function saveComentario() {
  try {
    const method = dialogMode.value === "add" ? "POST" : "PUT";
    const url =
      dialogMode.value === "add"
        ? "http://localhost:8000/comentarios/"
        : `http://localhost:8000/comentarios/${form.value.id}/`;

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form.value),
    });

    if (response.ok) {
      fetchComentarios();
      dialog.value = false;
    } else {
      console.error("Error al guardar comentario:", response.status);
    }
  } catch (error) {
    console.error("Error en saveComentario:", error);
  }
}

async function deleteComentario(comentario) {
  try {
    const response = await fetch(`http://localhost:8000/comentarios/${comentario.id}/`, {
      method: "DELETE",
    });

    if (response.ok) {
      fetchComentarios();
    } else {
      console.error("Error al eliminar comentario:", response.status);
    }
  } catch (error) {
    console.error("Error en deleteComentario:", error);
  }
}

onMounted(() => {
  fetchComentarios();
  fetchUsuarios();
});
</script>

<style scoped>
.v-btn {
  margin-left: 8px;
}
</style>
