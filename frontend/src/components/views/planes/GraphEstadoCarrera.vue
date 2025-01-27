<template>
  <div class="career-progress">
    <!-- Primera columna - Créditos -->
    <div class="column credits-column">
      <div class="credits-header">
        <font-awesome-icon :icon="['fas', 'book-open']" class="icon" />
        <h3>Créditos</h3>
      </div>
      <div class="credits-content">
        <span class="credits-obtained">{{ obtainedCredits }}</span>
        <span class="credits-separator">de</span>
        <span class="credits-total">{{ totalCredits }}</span>
      </div>
      <div class="percentage" :style="{ color: percentageColor }">
        {{ calculatedPercentage }}%
      </div>
    </div>

    <!-- Segunda columna - Barra de progreso -->
    <div class="column progress-column">
      <div class="progress-bar">
        <div
          v-for="(cycle, index) in cyclesProgress"
          :key="index"
          class="progress-segment"
          :style="{
            width: cycle.porcentaje + '%',
            backgroundColor: cycle.color
          }"
          @mouseover="showTooltip(cycle)"
          @mouseleave="hideTooltip"
        >
          <span class="segment-label">{{ cycle.nombre }} {{ cycle.porcentaje.toFixed(1) }}%</span>
        </div>
      </div>
      <div v-if="activeTooltip" class="progress-tooltip">
        {{ tooltipContent }}
      </div>
    </div>

    <!-- Tercera columna - Promedio -->
    <div class="column average-column">
      <div class="average-header">
        <font-awesome-icon :icon="['fas', 'medal']" class="icon" />
        <h3>Promedio</h3>
      </div>
      <div class="average-value">
        {{ formattedAverage }}
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue';
import { useCarreraStore } from '@/stores/CarreraStore';

export default {
  name: 'CareerProgress',
  setup() {
    const store = useCarreraStore();
    const activeTooltip = ref(false);
    const tooltipContent = ref('');

    // Carga inicial de datos
    onMounted(() => store.fetchEstadoCarrera());

    // Métodos para tooltip
    const showTooltip = (cycle) => {
      activeTooltip.value = true;
      tooltipContent.value = `${cycle.nombre}: ${cycle.creditos} créditos (${cycle.porcentaje.toFixed(1)}%)`;
    };

    const hideTooltip = () => {
      activeTooltip.value = false;
    };

    // Computed properties
    const obtainedCredits = computed(() => store.creditosAprobados);
    const totalCredits = computed(() => store.creditosTotales);
    const formattedAverage = computed(() => store.promedio?.toFixed(2) || '0.00');
    const cyclesProgress = computed(() => store.ciclosProgreso);

    const calculatedPercentage = computed(() => {
      return ((obtainedCredits.value / totalCredits.value) * 100 || 0).toFixed(1);
    });

    const percentageColor = computed(() => {
      const percentage = parseFloat(calculatedPercentage.value);
      if (percentage < 33) return '#e74c3c';
      if (percentage < 66) return '#f1c40f';
      return '#2ecc71';
    });

    return {
      obtainedCredits,
      totalCredits,
      formattedAverage,
      cyclesProgress,
      calculatedPercentage,
      percentageColor,
      activeTooltip,
      tooltipContent,
      showTooltip,
      hideTooltip
    };
  }
};
</script>

<style scoped>
/* Tus estilos existentes se mantienen igual */
.career-progress {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin: 1rem;
}

.column {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.credits-header, .average-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.icon {
  font-size: 1.5rem;
  color: #2c3e50;
}

.credits-content {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.credits-obtained {
  font-weight: 700;
  color: #2c3e50;
}

.credits-total {
  color: #7f8c8d;
}

.percentage {
  font-size: 1.5rem;
  font-weight: 700;
}

.progress-bar {
  width: 100%;
  height: 30px;
  background: #ecf0f1;
  border-radius: 15px;
  overflow: hidden;
  display: flex;
}

.progress-segment {
  height: 100%;
  transition: width 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.segment-label {
  color: white;
  font-size: 0.8rem;
  font-weight: 500;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.progress-tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.average-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .career-progress {
    grid-template-columns: 1fr;
  }
}
</style>