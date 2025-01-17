<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="10" md="8">
          <v-card>
            <v-card-title class="text-center">
              <h2 class="headline">Perfil de Usuario</h2>
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
                  </v-col>
                  <v-col cols="12" md="8">
                    <v-text-field
                      v-model="userData.username"
                      label="Nombre de usuario"
                      readonly
                      dense
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.email"
                      label="Email"
                      readonly
                      dense
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.first_name"
                      label="Nombre"
                      readonly
                      dense
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.last_name"
                      label="Apellido"
                      readonly
                      dense
                    ></v-text-field>

                    <v-text-field
                      v-model="userData.bio"
                      label="Biografía"
                      readonly
                      rows="3"
                      dense
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>

            <v-card-actions class="justify-center">
              <v-btn color="primary" :to="{ name: 'EditarPerfil' }">
                Editar Perfil
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>

  <script setup>
  import { ref, onMounted, computed } from "vue";

  const userData = ref(null);
  const loading = ref(false);
  const error = ref(null);

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
  </script>