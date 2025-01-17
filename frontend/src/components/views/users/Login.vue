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

                <v-alert v-if="error" type="error" dense text>
                  {{ error }}
                </v-alert>

                <v-btn type="submit" color="primary" block class="mt-2">
                  Iniciar Sesión
                </v-btn>
                <div class="text-center mt-3">
                  ¿No tenes una cuenta?
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
//   import { publicKey } from '@/api/auth'; // Importa la clave pública desde el archivo donde la obtuviste
//   import * as jose from 'jose';

  const router = useRouter();
  const username = ref('');
  const password = ref('');
  const error = ref(null);

  async function handleSubmit() {
    // try {
    //   // 1. Obtener la clave pública si aún no se ha cargado
    //   if (!publicKey.value) {
    //     console.error('La clave pública no está disponible.');
    //     error.value = 'Error al iniciar sesión. Inténtalo de nuevo más tarde.';
    //     return;
    //   }

    //   // 2. Enviar la solicitud de inicio de sesión al backend
    //   const response = await fetch('http://localhost:8000/iniciar-sesion', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({
    //       usuario: username.value,
    //       contraseña: password.value,
    //     }),
    //   });

    //   if (response.ok) {
    //     const data = await response.json();

    //     // 3. Verificar la firma del JWT usando la clave pública
    //     const isTokenValid = await verifyJWT(data.token);

    //     if (isTokenValid) {
    //       // 4. Guardar el token y la información del usuario en el localStorage o en un store
    //       localStorage.setItem('token', data.token);
    //       localStorage.setItem('user', JSON.stringify(data.info_usuario));
    //       // ... guardar otros datos como roles, etc.

    //       // 5. Redirigir al usuario a la página de inicio o a la página que intentaba acceder
    //       router.push({ name: 'Home' }); // Ajusta el nombre de la ruta según tu configuración
    //     } else {
    //       error.value = 'Token inválido. Por favor, inicia sesión de nuevo.';
    //     }
    //   } else {
    //     // Manejar errores de autenticación (credenciales incorrectas, etc.)
    //     const errorData = await response.json();
    //     error.value = errorData.message || 'Error de autenticación. Por favor, revisa tus credenciales.';
    //   }
    // } catch (err) {
    //   console.error('Error en el inicio de sesión:', err);
    //   error.value = 'Error al iniciar sesión. Inténtalo de nuevo más tarde.';
    // }
  }

//   async function verifyJWT(token) {
//     try {
//       const publicJWK = await jose.importSPKI(publicKey.value, 'RS256');
//       const { payload, protectedHeader } = await jose.jwtVerify(token, publicJWK, {
//         algorithms: ['RS256']
//       });
//       console.log("Cabecera protegida del JWT", protectedHeader);
//       console.log("Payload del JWT", payload);
//       return true;
//     } catch (err) {
//       console.error('Error al verificar el JWT:', err);
//       return false;
//     }
//   }
  </script>

  <style scoped>
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>