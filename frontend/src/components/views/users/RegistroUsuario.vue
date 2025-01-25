<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-center">Registro de Usuario</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="username"
                label="Usuario"
                prepend-icon="mdi-account"
                :rules="[required]"
                required
              ></v-text-field>

              <v-text-field
                v-model="email"
                label="Email"
                prepend-icon="mdi-email"
                :rules="[required, emailValid]"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Contraseña"
                prepend-icon="mdi-lock"
                type="password"
                :rules="[required, minLength]"
                required
              ></v-text-field>

              <v-alert v-if="error" type="error" dense text>
                {{ error }}
              </v-alert>

              <v-alert v-if="successMessage" type="success" dense text>
                {{ successMessage }}
              </v-alert>

              <v-btn type="submit" color="primary" block class="mt-2" :loading="isLoading">
                Registrarse
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/AuthStore';
import { api } from '@/services/apiServiceAuth';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const error = ref(null);
const successMessage = ref(null);
const isLoading = ref(false);
const authStore = useAuthStore();

onBeforeMount(() => {
  if (authStore.isAuthenticated) {
    router.push({ name: 'Home' }); // Redirige al inicio si ya está autenticado
  }
});

const required = (value) => !!value || 'Este campo es obligatorio.';
const emailValid = (value) => /.+@.+\..+/.test(value) || 'El email no es válido.';
const minLength = (value) => value.length >= 8 || 'La contraseña debe tener al menos 8 caracteres.';

async function handleSubmit() {
  isLoading.value = true;
  error.value = null;
  successMessage.value = null;

  try {
    const response = await api.post('usuarios/', { // Usa la función post de apiServiceAuth
      username: username.value,
      email: email.value,
      password: password.value, // Envía la contraseña sin codificar
    });

    if (response.status === 201) {
      successMessage.value = '¡Registro exitoso! Ahora puedes iniciar sesión.';
      error.value = null;
      username.value = '';
      email.value = '';
      password.value = '';
      setTimeout(() => {
        router.push({ name: 'Login' });
      }, 4000); // Redirige al login después de 4 segundos
    } else {
      error.value = 'Error en el registro. Por favor, inténtalo de nuevo.';
    }
  } catch (err) {
    console.error('Error en el registro:', err);
    error.value = 'Error al registrar el usuario. Inténtalo de nuevo más tarde.';
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 10px;
}
</style>