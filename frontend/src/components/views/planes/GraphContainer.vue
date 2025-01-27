<template>
  <div>
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
import { defineComponent, computed } from "vue";
import { useGraphStore } from "@store/GraphStore";
import GraphFilter from "./GraphFilter.vue";
import GraphMateriaDetalle from "./GraphMateriaDetalle.vue";
import { createChart, highlightConnections, resetHighlight } from "@utils/graphUtils";

export default defineComponent({
  name: "GraphContainer",
  components: {
    GraphFilter,
    GraphMateriaDetalle,
  },
  setup() {
    const store = useGraphStore();
    const selectedPlan = computed({
      get: () => store.selectedPlan,
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
</style>