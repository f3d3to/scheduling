<template>
  <v-container class="home-page fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card class="elevation-12 pa-12" outlined>
          <v-card-title class="text-center">
            <img class="logo" src="@/assets/icon.png" alt="Logo" />
            <h1 class="display-2 font-weight-bold">
              Bienvenido a ESTUDI-AR
            </h1>
          </v-card-title>
          <v-card-subtitle class="text-center mt-4">
            <p class="text-body-1">
              Gestioná tus proyectos con esta aplicación.
            </p>
          </v-card-subtitle>
          <v-card-actions class="justify-center mt-6">
            <v-btn color="primary" size="x-large" to="/planes" variant="flat">
              Empezá ahora
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>Bienvenido a ESTUDI-AR !

<script>
import { onUnmounted } from 'vue';
import { push, updateConfig } from 'notivue';
import { sendNotificationWithCustomConfig } from '@/utils/notificationHelper';
export default {
  name: "HomePage",
  mounted() {
    sendNotificationWithCustomConfig({
      component: "WelcomeNotification",
      props: {
        title: '¡Bienvenido a ESTUDI-AR!',
        subtitle: 'Comienza a gestionar tus proyectos de forma eficiente. Explora las funcionalidades y si necesitas ayuda, consulta la sección de Ayuda.',
        icon: 'mdi mdi-rocket-launch',
        color: "green",},
    }, {position: 'top-center'}
  );
  }
};
</script>

<style scoped>

.logo {
  height: 80px; /* Ajusta el tamaño del logo */
}

.home-page {
  color: white;
  font-family: "Roboto", sans-serif;
}

.v-card-subtitle p {
  font-size: 1.3rem; /* Ajusta el tamaño del texto */
  line-height: 1.8; /* Ajusta el interlineado */
}

.v-btn {
  text-transform: none; /* Quita la transformación a mayúsculas */
  letter-spacing: normal; /* Ajusta el espaciado entre letras */
  font-weight: 600; /* Ajusta el grosor de la fuente */
}

.text-decoration-none {
  text-decoration: none;
}
</style>