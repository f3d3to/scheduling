<template>
  <div id="app">
    <Sidebar />
    <div class="content-wrapper">
      <TopBar @filter-change="onFilterChange" />
      <div class="content">
        <GraphContainer :filter-text="filterText" />
      </div>
    </div>
  </div>
</template>


<script>
import GraphContainer from "./components/GraphContainer.vue";
import TopBar from "./components/TopBar.vue";
import Sidebar from "./components/SideBar.vue";

export default {
  name: "App",
  components: {
    GraphContainer,
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

#app {
  display: flex; /* Layout principal con flexbox */
  height: 100vh; /* Ocupa toda la ventana */
  overflow: hidden; /* Previene desbordamientos */
}

.sidebar {
  width: 250px; /* Ancho fijo para el Sidebar */
  height: 100%; /* Asegura que ocupe toda la altura */
  background-color: #333;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 10px;
  transition: transform 0.3s ease;
  flex-shrink: 0; /* Evita que cambie de tamaño */
}

.sidebar.is-hidden {
  transform: translateX(-100%); /* Oculta el Sidebar */
}

.content-wrapper {
  flex: 1; /* El resto del espacio lo ocupa Content */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Previene desbordamiento del gráfico */
}

.topbar {
  height: 60px; /* Altura fija para la barra superior */
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  flex-shrink: 0; /* No permite colapsar */
}

.content {
  flex: 1; /* Ocupa el espacio restante */
  display: flex;
  overflow: hidden; /* Evita scroll no deseado */
}


</style>
