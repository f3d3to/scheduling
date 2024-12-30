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
import TopBar from "@common/TopBar.vue";
import Sidebar from "@common/SideBar.vue";

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


/* Estilo general para los botones */
.btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
}

/* Botón de Editar */
.btn-editar {
  background-color: #007bff; /* Azul */
  color: white;
}
.btn-editar:hover {
  background-color: #0056b3; /* Azul más oscuro al pasar el mouse */
}
.container .vue-grid-item.vue-grid-placeholder {
    background: green !important;
}

/* Botón de Guardar */
.btn-guardar {
  background-color: #28a745; /* Verde */
  color: white;
}
.btn-guardar:hover {
  background-color: #218838; /* Verde más oscuro al pasar el mouse */
}

</style>
