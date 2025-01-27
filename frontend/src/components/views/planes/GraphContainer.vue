<template>
  <div>
    <GraphEstadoCarrera />
    <div ref="chart" class="graph-container">
      <GraphFilter
        :plans="store.plans"
        :selectedPlan="selectedPlan"
        @update:selectedPlan="handlePlanChange"
        @filter-changed="handleFilterChanged"
        class="floating-filter"
      />
    </div>

    <GraphMateriaDetalle
      v-show="selectedMateria"
      :selectedMateria="selectedMateria"
      @close-detail="closeDetail"
      @update-node-color="updateNodeColor"
    />

  </div>
</template>

<script>
import { defineComponent, computed, ref } from "vue";
import { useGraphStore } from "@store/GraphStore";
import GraphFilter from "./GraphFilter.vue";
import GraphMateriaDetalle from "./GraphMateriaDetalle.vue";
import GraphEstadoCarrera from "./GraphEstadoCarrera.vue";
import { createChart, highlightConnections, resetHighlight } from "@utils/graphUtils";

export default defineComponent({
  name: "GraphContainer",
  components: {
    GraphFilter,
    GraphMateriaDetalle,
    GraphEstadoCarrera
  },
  setup() {
    const store = useGraphStore();
    const selectedPlan = computed({
      get: () => store.selectedPlan || store.plans[0]?.id || null, // <-- Default al primer plan
      set: (value) => {
        store.selectedPlan = value;
      },
    });

    return { store, selectedPlan };
  },
  data() {
    return {
      activeFilters: {},
      estadosOptions: [
        { text: "Aprobada", value: "aprobado" },
        { text: "Cursando", value: "cursando" },
        { text: "No Cursada", value: "no_cursada" },
      ],
      selectedMateria: null,
    };
  },
  async mounted() {
    try {
      await this.store.fetchPlans();
      if (this.store.plans.length > 0) {
        await this.fetchSelectedPlan();
      }
    } catch (error) {
      console.error("Error fetching plans:", error);
    }
  },
  methods: {
    async fetchSelectedPlan() {
      if (!this.selectedPlan) return;

      try {
        await this.store.fetchCycles({ condicion: "carrera" });
        this.createChart();
      } catch (error) {
        console.error("Error fetching plan cycles:", error);
      }
    },
    async handleFilterChanged(filters) {
      try {
        const { promocionadas, disponibles, ...backendFilters } = filters;
        await this.store.fetchCycles(filters);

        this.createChart(promocionadas);
      } catch (error) {
        console.error("Error applying filters:", error);
      }
    },
    handlePlanChange(newPlan) {
      this.selectedPlan = newPlan;
      this.fetchSelectedPlan();
    },
    createChart(promocionadas) {
      createChart(this.$refs.chart, this.store.nodes, this.store.links, promocionadas, this.highlightConnections, this.resetHighlight);
    },
    highlightConnections(selectedNode) {
      highlightConnections(selectedNode, this.store.nodes, this.store.links);
      this.selectedMateria = selectedNode;
    },
    resetHighlight() {
      resetHighlight();
    },
    closeDetail() {
      this.selectedMateria = null;
    },
    updateNodeColor(nodeId, color) {
      const node = this.store.nodes.find((n) => n.id === nodeId);
      if (node) {
        node.customColor = color;
        this.createChart();
      }
    },
  },
});
</script>

<style scoped>
svg {
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}

.nodes circle {
  cursor: pointer;
}

.labels text {
  font-weight: bold;
  font-size: 12px;
  fill: #ffffff;
  text-anchor: middle;
}

.year-group {
  fill: rgba(136, 136, 136, 0.1);
}
.bottom-panel {
  position: fixed;
  bottom: -100%;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 800px;
  background: white;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  transition: bottom 0.3s ease;
  z-index: 1000;
}

.panel-visible {
  bottom: 0;
}

.toggle-wrapper {
  display: flex;
  justify-content: center;
  margin-top: -28px; /* Mitad del botón fuera del panel */
}

.toggle-btn {
  transition: transform 0.3s ease;
}

.toggle-btn:hover {
  transform: scale(1.1);
}
</style>