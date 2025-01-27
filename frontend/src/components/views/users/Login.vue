<template>
  <v-container class="h-100">
    <v-row justify="center" align="center" class="h-100">
      <v-col cols="12" sm="8" md="6">
        <v-card class="login-card">
          <v-card-title class="text-center login-title">Iniciar Sesión</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="username"
                label="Usuario"
                prepend-icon="mdi-account"
                :rules="[required]"
                required
                class="login-input"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Contraseña"
                prepend-icon="mdi-lock"
                type="password"
                :rules="[required]"
                required
                class="login-input"
              ></v-text-field>

              <v-alert v-if="authStore.error" type="error" dense text class="login-error">
                {{ authStore.error }}
              </v-alert>

              <v-btn type="submit" color="primary" block class="mt-2 login-button" :loading="authStore.isLoading">
                Iniciar Sesión
              </v-btn>
              <div class="text-center mt-3 login-link">
                ¿No tenés una cuenta?
                <router-link :to="{ name: 'RegistroUsuario' }" class="login-link-text">
                  Regístrate acá
                </router-link>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/AuthStore';

const router = useRouter();
const username = ref('');
const password = ref('');
const authStore = useAuthStore();

const required = value => !!value || 'Este campo es obligatorio.';

async function handleSubmit() {
  try {
    await authStore.login({ username: username.value, password: password.value });
    router.push({ name: 'Home' });
  } catch (error) {
    console.error("Error en el inicio de sesión:", error);
  }
}
</script>

<style scoped>
.login-card {
  background: linear-gradient(180deg, #2c2c3e, #1e1e2f);
  color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.login-input {
  background-color: #3a3a4e;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 16px;
}

.login-input .v-input__control {
  color: #fff;
}

.login-input .v-label {
  color: #fff !important;
}

.login-input .v-icon {
  color: #fff;
}

.login-error {
  background-color: #ff4444;
  color: #fff;
  border-radius: 8px;
  padding: 8px;
  margin-bottom: 16px;
}

.login-button {
  background-color: #4caf50;
  color: #fff;
  border-radius: 8px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #45a049;
}

.login-link {
  color: #fff;
  font-size: 14px;
}

.login-link-text {
  color: #4caf50;
  text-decoration: none;
  font-weight: bold;
}

.login-link-text:hover {
  text-decoration: underline;
}

.h-100 {
  height: 100%;
}
</style>