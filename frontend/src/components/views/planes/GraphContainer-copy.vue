<template>
    <div class="graph-container">
      <!-- Selector de Plan -->
      <select
        v-model="store.selectedPlan"
        @change="store.fetchCycles(store.selectedPlan!)"
      >
        <option
          v-for="plan in store.plans"
          :key="plan.id"
          :value="plan.id"
        >
          {{ plan.nombre }}
        </option>
      </select>

      <!-- Contenedor del Gráfico -->
      <div ref="chart" class="d3-chart"></div>

      <!-- Panel de Detalles (implementar luego) -->
      <MateriaDetalle v-if="store.selectedMateria" />
    </div>
  </template>

  <script setup lang="ts">
  import { useGraphStore } from '@/store/graphStore';
  import { onMounted, ref } from 'vue';
  import * as d3 from 'd3';

  const store = useGraphStore();
  const chart = ref<HTMLElement>();

  onMounted(async () => {
    await store.fetchPlans();
    if (store.plans.length > 0) {
      store.selectedPlan = store.plans[0].id;
      await store.fetchCycles(store.selectedPlan);
      initializeD3();
    }
  });

  const initializeD3 = () => {
    // Copia tu método createChart() aquí, adaptando:
    // - Reemplaza this.$refs.chart por chart.value
    // - Usa store.nodes y store.links
  };
  </script>