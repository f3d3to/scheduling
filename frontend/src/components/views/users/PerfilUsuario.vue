<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8">
        <v-card>
          <v-card-title class="text-center">
            <h2 class="headline">Perfil de Usuario</h2>
          </v-card-title>

          <v-card-text>
            <v-alert v-if="authStore.isLoading" type="info" text>
              Cargando información del perfil...
            </v-alert>

            <v-alert v-if="authStore.error" type="error" dense text>
              {{ authStore.error }}
            </v-alert>

            <div v-if="authStore.user">
              <v-row>
                <v-col cols="12" md="4" class="text-center">
                  <v-avatar size="150" v-if="authStore.user.profile_picture">
                    <v-img :src="authStore.user.profile_picture" aspect-ratio="1"></v-img>
                  </v-avatar>
                  <v-avatar size="150" v-else color="primary">
                    <span class="white--text text-h5">{{ userInitial }}</span>
                  </v-avatar>
                </v-col>
                <v-col cols="12" md="8">
                  <p>
                    <strong>Nombre de usuario:</strong>
                    {{ authStore.user.username }}
                  </p>
                  <p>
                    <strong>Email:</strong>
                    {{ authStore.user.email }}
                  </p>
                  <p>
                    <strong>Perfil:</strong>
                    {{ authStore.user.perfil }}
                  </p>
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
import { computed, onMounted } from "vue";
import { useAuthStore } from "@/store/AuthStore";

const authStore = useAuthStore();

onMounted(() => {
  if (!authStore.isAuthenticated) {
    authStore.checkAuth();
  }
});

const userInitial = computed(() => {
  return authStore.user?.username.charAt(0).toUpperCase() ?? "";
});
</script>