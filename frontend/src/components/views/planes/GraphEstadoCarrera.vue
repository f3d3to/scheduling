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
              width: cycle.percentage + '%',
              backgroundColor: cycle.color
            }"
            @mouseover="showTooltip(cycle)"
            @mouseleave="hideTooltip"
          >
            <span class="segment-label">{{ cycle.name }} {{ cycle.percentage }}%</span>
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
  import { computed, ref } from 'vue';
  import { useStore } from '@/stores/mainStore';

  export default {
    name: 'CareerProgress',
    setup() {
      const store = useStore();
      const activeTooltip = ref(false);
      const tooltipContent = ref('');

      // Cálculo de créditos
      const obtainedCredits = computed(() =>
        store.courses.reduce((sum, course) =>
          course.approved ? sum + course.credits : sum, 0)
      );

      const totalCredits = computed(() =>
        store.courses.reduce((sum, course) => sum + course.credits, 0)
      );

      const calculatedPercentage = computed(() =>
        ((obtainedCredits.value / totalCredits.value) * 100).toFixed(2)
      );

      // Colores y porcentaje por ciclo
      const cycleColors = {
        'CBC': '#4CAF50',
        'OBLIGATORIAS': '#2196F3',
        'ELECTIVAS': '#9C27B0',
        'INGLÉS': '#FFEB3B',
        'TIF': '#F44336'
      };

      const cyclesProgress = computed(() => {
        const cycles = store.courses.reduce((acc, course) => {
          if (!acc[course.cycle]) {
            acc[course.cycle] = {
              total: 0,
              obtained: 0
            };
          }
          acc[course.cycle].total += course.credits;
          if (course.approved) acc[course.cycle].obtained += course.credits;
          return acc;
        }, {});

        return Object.entries(cycles).map(([name, data]) => ({
          name,
          percentage: ((data.obtained / data.total) * 100).toFixed(2),
          color: cycleColors[name] || '#607D8B',
          credits: `${data.obtained}/${data.total}`
        }));
      });

      // Cálculo del promedio
      const studentAverage = computed(() => {
        const validCourses = store.courses.filter(course => course.grade);
        if (validCourses.length === 0) return 0;

        const total = validCourses.reduce((sum, course) =>
          sum + parseFloat(course.grade), 0);

        return total / validCourses.length;
      });

      const formattedAverage = computed(() =>
        studentAverage.value.toFixed(2)
      );

      // Tooltip interactivo
      const showTooltip = (cycle) => {
        tooltipContent.value = `Créditos obtenidos: ${cycle.credits}`;
        activeTooltip.value = true;
      };

      const hideTooltip = () => {
        activeTooltip.value = false;
      };

      return {
        obtainedCredits,
        totalCredits,
        calculatedPercentage,
        percentageColor: computed(() =>
          calculatedPercentage.value >= 50 ? '#4CAF50' : '#F44336'),
        cyclesProgress,
        formattedAverage,
        activeTooltip,
        tooltipContent,
        showTooltip,
        hideTooltip
      };
    }
  };
  </script>

  <style scoped>
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