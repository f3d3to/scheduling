<template>
  <div>
    <!-- Botón fijo para mostrar/ocultar la sidebar -->
    <button
      class="fixed-btn"
      :class="{ 'shifted': isVisible }"
      @click="toggleSidebar"
    >
      <i :class="isVisible ? 'fas fa-angle-left' : 'fas fa-angle-right'"></i>
    </button>

    <!-- Sidebar -->
    <div :class="['sidebar', { 'is-hidden': !isVisible }]">
      <nav>
        <ul>
          <li><RouterLink to="/"><i class="fas fa-home"></i> Inicio</RouterLink></li>
          <li><RouterLink to="/planes"><i class="fa-solid fa-network-wired"></i>Planes de estudio</RouterLink></li>
          <li><RouterLink to="/timer"><i class="fas fa-clock"></i> Timer</RouterLink></li>
          <li><RouterLink to="/planificadores"><i class="fas fa-calendar-alt"></i> Planificadores</RouterLink></li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: "SideBar",
  data() {
    return {
      isVisible: true,
    };
  },
  methods: {
    toggleSidebar() {
      this.isVisible = !this.isVisible;
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background: linear-gradient(180deg, #2c2c3e, #1e1e2f);
  color: #fff;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
  z-index: 1001; /* Asegura que esté encima del contenido */
}

.sidebar.is-hidden {
  transform: translateX(-100%);
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar nav li {
  margin-bottom: 20px;
}

.sidebar nav a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 10px 15px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.sidebar nav a:hover {
  background-color: #535bf2;
}

.fixed-btn {
  position: fixed;
  top: 15px;
  left: 15px;
  background-color: #2c2c3e;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 1002; /* Asegura que esté encima de la sidebar */
  transition: all 0.3s ease;
}

/* Cambia la posición del botón cuando la sidebar está visible */
.fixed-btn.shifted {
  left: 270px; /* Alinea con el borde derecho de la sidebar */
}

.fixed-btn:hover {
  background-color: #535bf2;
}

.fixed-btn i {
  font-size: 1.2rem;
}
</style>
