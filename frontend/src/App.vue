<template>
  <div id="app">
    <GraphContainer />
  </div>
</template>

<script>
import GraphContainer from "./components/GraphContainer.vue";

export default {
  name: "App",
  components: {
    GraphContainer,
  },
};
</script>

<style>
/* Aplica estilos globales aquí si es necesario */
#app {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
