<template>
  <v-card>
    <v-tabs v-model="activeTab" color="primary" grow>
      <v-tab value="annual">Anual</v-tab>
      <v-tab value="monthly">Mensual</v-tab>
      <v-tab value="weekly">Semanal</v-tab>
      <v-tab value="daily">Diario</v-tab>
      <v-tab value="list">Listado</v-tab>

    </v-tabs>

    <v-window v-model="activeTab">
      <v-window-item value="annual">
        <Anual />
      </v-window-item>

      <v-window-item value="monthly">
        <Mensual />
      </v-window-item>

      <v-window-item value="weekly">
        <Semanal />
      </v-window-item>

      <v-window-item value="daily">
        <Dia />
      </v-window-item>

      <v-window-item value="list">
        <Listado />
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCalendarStore } from "@store/CalendarioStore";
import Anual from "./Anual.vue";
import Mensual from "./Mensual.vue";
import Semanal from "./Semanal.vue";
import Dia from "./Dia.vue";
import Listado from "./Listado.vue";

const activeTab = ref("annual");
const store = useCalendarStore();

onMounted(async () => {
  await store.fetchEvents(); // Cargar eventos al montar
});
</script>

<style scoped>
.fc {
  height: 70vh;
  margin: 20px;
}
</style>