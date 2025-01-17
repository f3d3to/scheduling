<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="10" md="8">
          <v-card>
            <v-card-title class="text-center">
              <h2 class="headline">Editar Perfil</h2>
            </v-card-title>

            <v-card-text>
              <v-alert v-if="loading" type="info" text>
                Cargando información del perfil...
              </v-alert>

              <v-alert v-if="error" type="error" dense text>
                {{ error }}
              </v-alert>

              <div v-if="userData">
                <v-row>
                  <v-col cols="12" md="4" class="text-center">
                    <v-avatar size="150" v-if="userData.profile_picture">
                      <v-img :src="userData.profile_picture" aspect-ratio="1"></v-img>
                    </v-avatar>
                    <v-avatar size="150" v-else color="primary">
                      <span class="white--text text-h5">{{ userInitial }}</span>
                    </v-avatar>
                    <input
                      type="file"
                      @change="onFileSelected"
                      class="mt-4"
                    />
                  </v-col>
                  <v-col cols="12" md="8">
                    <v-text-field
                      v-model="userData.username"
                      label="Nombre de usuario"
                      :rules="[required]"
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.email"
                      label="Email"
                      :rules="[required, emailValid]"
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.first_name"
                      label="Nombre"
                      :rules="[required]"
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.last_name"
                      label="Apellido"
                      :rules="[required]"
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.bio"
                      label="Biografía"
                      rows="3"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-divider class="my-4"></v-divider>
                    <h3 class="text-h6 mb-4">Cambiar Contraseña</h3>
                    <v-text-field
                      v-model="currentPassword"
                      label="Contraseña actual"
                      type="password"
                      :rules="[required]"
                    ></v-text-field>

                    <v-text-field
                      v-model="newPassword"
                      label="Nueva contraseña"
                      type="password"
                      :rules="[required, minLength]"
                    ></v-text-field>

                    <v-text-field
                      v-model="confirmNewPassword"
                      label="Confirmar nueva contraseña"
                      type="password"
                      :rules="[required, passwordsMatch]"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>

            <v-card-actions class="justify-center">
              <v-btn
                color="success"
                @click="saveProfile"
                :disabled="!userData.username || !userData.email || !userData.first_name || !userData.last_name"
              >
                Guardar Cambios
              </v-btn>
              <v-btn color="error" @click="cancelEdit">
                Cancelar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted, computed } from "vue";
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const userData = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const currentPassword = ref("");
  const newPassword = ref("");
  const confirmNewPassword = ref("");
  const selectedFile = ref(null);

  const required = (value) => !!value || "Este campo es obligatorio.";
  const emailValid = (value) =>
    /.+@.+\..+/.test(value) || "El email no es válido.";
  const minLength = (value) =>
    (value && value.length >= 8) || "Mínimo 8 caracteres.";
  const passwordsMatch = (value) =>
    value === newPassword.value || "Las contraseñas no coinciden.";

  const userInitial = computed(() => {
    if (userData.value && userData.value.first_name) {
      return userData.value.first_name.charAt(0).toUpperCase();
    }
    return "";
  });

  onMounted(() => {
    // Simulación de carga de datos del usuario
    setTimeout(() => {
      userData.value = {
        username: "usuarioEjemplo",
        email: "ejemplo@email.com",
        first_name: "Nombre",
        last_name: "Apellido",
        bio: "Una breve biografía sobre mí.",
        profile_picture: null, // URL de la imagen de perfil o null
      };
      loading.value = false;
    }, 1000);
  });

  function saveProfile() {
    // Aquí implementarías la lógica para guardar los cambios en el backend
    console.log("Guardando cambios:", userData.value);

    // Ejemplo de cómo podrías enviar la imagen al backend:
    if (selectedFile.value) {
      const formData = new FormData();
      formData.append("profile_picture", selectedFile.value);
      // ... enviar formData al backend
    }

    // Lógica para cambiar la contraseña si se ha introducido una nueva
    if (newPassword.value) {
      if (currentPassword.value && newPassword.value === confirmNewPassword.value) {
        console.log("Cambiando contraseña...");
        // Aquí implementarías la lógica para enviar la solicitud de cambio de contraseña al backend
      } else {
        error.value = "Las contraseñas no coinciden o la contraseña actual es incorrecta.";
        return;
      }
    }
      router.push({ name: 'PerfilUsuario' });
  }

  function cancelEdit() {
    currentPassword.value = "";
    newPassword.value = "";
    confirmNewPassword.value = "";
    selectedFile.value = null;
      router.push({ name: 'PerfilUsuario' });
  }

  function onFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
      selectedFile.value = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        userData.value.profile_picture = e.target.result;
      };
      reader.readAsDataURL(file);
    } else {
      selectedFile.value = null;
    }
  }
  </script>