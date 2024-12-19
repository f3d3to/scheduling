<template>
  <div>
    <!-- Botón siempre visible para mostrar el sidebar -->
    <button class="toggle-btn fixed-btn" @click="toggleSidebar">
      {{ isVisible ? 'Ocultar' : 'Mostrar' }}
    </button>

    <!-- Sidebar -->
    <div :class="['sidebar', { 'is-hidden': !isVisible }]">
      <nav v-if="isVisible">
        <ul>
          <li><a href="#home">Inicio</a></li>
          <li><a href="#about">Acerca de</a></li>
          <li><a href="#services">Servicios</a></li>
          <li><a href="#contact">Contacto</a></li>
        </ul>
      </nav>
    </div>
  </div>
</template>


<script>
export default {
  name: "Sidebar",
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
  background-color: #333;
  color: #fff;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  padding: 10px;
  transition: transform 0.3s ease;
}

.sidebar.is-hidden {
  transform: translateX(-100%);
}

.toggle-btn {
  background-color: #444;
  color: #fff;
  border: none;
  padding: 10px;
  cursor: pointer;
  text-align: center;
  margin-bottom: 20px;
}

.toggle-btn:hover {
  background-color: #555;
}

/* Botón fijo visible en todo momento */
.fixed-btn {
  position: fixed;
  top: 10px;
  left: 10px; /* Cambiar si necesitas ajustar la posición */
  z-index: 1000; /* Asegura que esté sobre otros elementos */
}

nav ul {
  list-style: none;
  padding: 0;
}

nav li {
  margin: 10px 0;
}

nav a {
  text-decoration: none;
  color: #fff;
  font-size: 16px;
}

nav a:hover {
  text-decoration: underline;
}

</style>
