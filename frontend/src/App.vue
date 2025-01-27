<template>
<v-app>
  <div class="notifications">
    <Notivue v-slot="item" >
      <template v-if="item.component === 'WelcomeNotification'">
        <WelcomeNotification :item="item"/>
      </template>
      <template v-else>
        <Notification :item="item" :theme="materialTheme" />
      </template>
    </Notivue>
  </div>
  <TopBar @filter-change="onFilterChange" />
  <Sidebar />
  <div class="content-wrapper overflow-y-auto" >
    <div class="content">
      <router-view />
    </div>
  </div>
</v-app>
</template>

<script>
import TopBar from "@common/TopBar.vue";
import Sidebar from "@common/SideBar.vue";


import { Notivue, Notification, materialTheme } from 'notivue'
import WelcomeNotification from '@views/custom-notificaciones/WelcomeNotification.vue';
export default {
  name: "App",
  components: {
    TopBar,
    Sidebar,
    Notivue,
    Notification,
    WelcomeNotification,

  },
  data() {
    return {
      filterText: "",
      materialTheme: materialTheme,
    };
  },
  methods: {
    onFilterChange(filterValue) {
      this.filterText = filterValue;
    },
  },
};
</script>

<style>
.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.content {
  flex: 1;
  display: block; /* Cambiar a block para evitar interferencias */
  justify-content: flex-start; /* Alinear al inicio */
  align-items: flex-start;
}

.content > router-view {
  flex: 1;
  display: flex; /* Habilita flexbox dentro del router-view */
  justify-content: center; /* Centra el contenido del temporizador */
  align-items: center;
  width: 100%; /* Asegura que ocupa todo el ancho */
  height: 100%; /* Asegura que ocupa todo el alto */
}

#app {
  display: flex;
  height: 100vh; /* Asegura que ocupe toda la pantalla */
  overflow: hidden;
}

.sidebar {
  width: 250px;
  height: 100%; /* Sidebar ocupa toda la altura */
  background-color: #333;
  color: #fff;
}

</style>
