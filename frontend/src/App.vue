<template>
  <Sidebar />
  <div class="content-wrapper overflow-y-auto" >
    <TopBar @filter-change="onFilterChange" />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import TopBar from "./components/TopBar.vue";
import Sidebar from "./components/SideBar.vue";

export default {
  name: "App",
  components: {
    TopBar,
    Sidebar,
  },
  data() {
    return {
      filterText: "",
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
  padding: 20px; /* Opcional: agrega espacio alrededor del contenido */
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
