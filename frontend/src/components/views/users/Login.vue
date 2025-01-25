<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-center">Iniciar Sesión</v-card-title>
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
                v-model="password"
                label="Contraseña"
                prepend-icon="mdi-lock"
                type="password"
                :rules="[required]"
                required
              ></v-text-field>

              <v-alert v-if="authStore.error" type="error" dense text>
                {{ authStore.error }}
              </v-alert>

              <v-btn type="submit" color="primary" block class="mt-2" :loading="authStore.isLoading">
                Iniciar Sesión
              </v-btn>
              <div class="text-center mt-3">
                ¿No tenés una cuenta?
                <router-link :to="{ name: 'RegistroUsuario' }">
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
    router.push({ name: 'Home' }); // Redirige al inicio después del login exitoso
  } catch (error) {
    // Los errores ya se manejan en el store, solo necesitas esta parte si quieres hacer algo más
    console.error("Error en el inicio de sesión:", error);
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 10px;
}
</style>