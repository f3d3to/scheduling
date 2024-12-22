<template>
    <div class="home-page">
      <section class="intro">
        <h1>Bienvenido a Mi Aplicación</h1>
        <p>
          Gestiona tus proyectos y productividad con nuestra aplicación. Explora
          funciones intuitivas y herramientas avanzadas.
        </p>
      </section>

      <!-- Gestión de Estados -->
      <section class="estado-management">
        <h2>Gestión de Estados</h2>
        <EstadoComponent />
      </section>
    </div>
  </template>

  <script>
  import EstadoComponent from "./Estados.vue";

  export default {
    name: "HomePage",
    components: {
      EstadoComponent,
    },
  };
  </script>

  <style scoped>
  .home-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 100%;
    padding: 20px;
    color: #fff;
    font-family: "Inter", sans-serif;
    background: linear-gradient(180deg, #1e1e2f, #2c2c3e);
  }

  .intro {
    margin-bottom: 40px;
  }

  .intro h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
  }

  .intro p {
    font-size: 1.2rem;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.7);
  }

  .estado-management {
    width: 100%;
    max-width: 800px;
    margin-top: 40px;
    padding: 20px;
    background-color: #2c2c3e;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }

  .estado-management h2 {
    font-size: 1.8rem;
    margin-bottom: 20px;
    color: #fff;
    text-align: center;
  }
  </style>
