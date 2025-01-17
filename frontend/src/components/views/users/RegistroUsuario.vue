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

                <v-btn type="submit" color="primary" block class="mt-2">
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
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const username = ref('');
  const email = ref('');
  const password = ref('');
  const error = ref(null);
  const successMessage = ref(null);

  const required = value => !!value || 'Este campo es obligatorio.';
  const emailValid = value => /.+@.+\..+/.test(value) || 'El email no es válido.';
  const minLength = value => value.length >= 8 || 'La contraseña debe tener al menos 8 caracteres.';

  async function handleSubmit() {
    try {
      const response = await fetch('http://localhost:8000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          usuario: username.value,
          email: email.value,
          contraseña: password.value,
        }),
      });

      if (response.ok) {
        successMessage.value = '¡Registro exitoso! Ahora puedes iniciar sesión.';
        error.value = null;
        username.value = '';
        email.value = '';
        password.value = '';
        setTimeout(() => {
          router.push({ name: 'Login' });
        }, 4000); // Redirige al login después de 4 segundos
      } else {
        const errorData = await response.json();
        error.value = errorData.message || 'Error en el registro. Por favor, inténtalo de nuevo.';
        successMessage.value = null;
      }
    } catch (err) {
      console.error('Error en el registro:', err);
      error.value = 'Error al registrar el usuario. Inténtalo de nuevo más tarde.';
      successMessage.value = null;
    }
  }
  </script>