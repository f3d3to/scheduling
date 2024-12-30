<template>
    <div class="home-page">
      <section class="intro">
        <h1>Bienvenido a Mi Aplicación</h1>
        <p>
          Gestiona tus proyectos y productividad con nuestra aplicación. Explora
          funciones intuitivas y herramientas avanzadas.
        </p>
      </section>
    </div>
  </template>

  <script>

  export default {
    name: "HomePage",
  };
  </script>

  <style scoped>
  .home-page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 100%;
    padding: 20px;
    color: #212132;
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
  </style>
