<template>
    <div class="career-status" v-if="visible">
      <div class="header">
        <h3>Progreso de la Carrera</h3>
        <button @click="toggleVisibility" class="toggle-btn">×</button>
      </div>

      <div class="stats-container">
        <!-- Columna Izquierda -->
        <div class="stat-column">
          <div class="stat-card">
            <h4>Création (2)</h4>
            <div class="credits-section">
              <p class="main-credits">50 de 226 <span class="total-credits">[255]</span></p>
              <div class="percentage-bar">
                <div class="progress" :style="{ width: realPercentage + '%' }"></div>
              </div>
              <p class="percentage">{{ realPercentage.toFixed(1) }}%</p>
            </div>

            <div class="additional-info">
              <p>FMC <span>12</span></p>
              <p>RELATIONNAI <span>8</span></p>
              <p>RECONNÉ <span>6</span></p>
              <p>PRIOR <span>10</span></p>
              <p>IPE <span>14</span></p>
            </div>
          </div>
        </div>

        <!-- Columna Derecha -->
        <div class="stat-column">
          <div class="stat-card">
            <h4>Promedio</h4>
            <div class="average-section">
              <p class="average-value">{{ formattedRealAverage }}</p>
              <div class="simulated-average">
                <span>Simulado: {{ formattedSimulatedAverage }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script>
  import { defineComponent } from 'vue';
  import { useGraphStore } from '@store/GraphStore';

  export default defineComponent({
    name: 'GraphEstadoCarrera',
    props: {
      visible: {
        type: Boolean,
        default: true
      }
    },
    setup() {
      const store = useGraphStore();
      return { store };
    },
    computed: {
      // Mantener los cálculos anteriores y añadir:
      totalRequiredCredits() {
        return 226; // Ejemplo estático - deberías obtenerlo del store
      },
      realPercentage() {
        return (this.realCompletedCredits / this.totalRequiredCredits) * 100;
      },
      // ... otros computed properties
    },
    methods: {
      toggleVisibility() {
        this.$emit('update:visible', !this.visible);
      }
    }
  });
  </script>

  <style scoped>
  .career-status {
    position: absolute;
    top: 20px;
    left: 20px;
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    width: 320px;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }

  .toggle-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
  }

  .stats-container {
    display: flex;
    gap: 15px;
  }

  .stat-column {
    flex: 1;
  }

  .stat-card h4 {
    color: #2c3e50;
    margin: 0 0 10px 0;
    font-size: 14px;
  }

  .credits-section {
    margin-bottom: 15px;
  }

  .main-credits {
    font-size: 18px;
    font-weight: bold;
    margin: 0;
  }

  .total-credits {
    color: #95a5a6;
    font-size: 14px;
  }

  .percentage-bar {
    height: 6px;
    background: #ecf0f1;
    border-radius: 3px;
    margin: 8px 0;
  }

  .progress {
    height: 100%;
    background: #3498db;
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .percentage {
    font-size: 14px;
    color: #7f8c8d;
    margin: 0;
  }

  .additional-info p {
    display: flex;
    justify-content: space-between;
    margin: 6px 0;
    font-size: 12px;
    color: #34495e;
  }

  .average-section {
    text-align: center;
    padding: 15px 0;
  }

  .average-value {
    font-size: 28px;
    font-weight: bold;
    color: #27ae60;
    margin: 0;
  }

  .simulated-average {
    margin-top: 10px;
    font-size: 12px;
    color: #95a5a6;
  }
  </style>