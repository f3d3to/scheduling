<template>
  <div>
    <!-- <v-container fluid>
      <v-row>
        <v-col cols="12" md="3">
          <v-select
            v-model="selectedPlan"
            :items="store.plans"
            item-title="nombre"
            item-value="id"
            label="Seleccionar Plan"
            @update:modelValue="fetchSelectedPlan"
          ></v-select>
        </v-col>
      </v-row>
    </v-container> -->

    <div ref="chart" class="graph-container">
      <GraphFilter
        :plans="store.plans"
        :selectedPlan="selectedPlan"
        @update:selectedPlan="handlePlanChange"
        @filter-changed="handleFilterChanged"
        class="floating-filter"
      />
    </div>

    <!-- Mostrar GraphMateriaDetalle si hay una materia seleccionada -->
    <GraphMateriaDetalle
      v-show="selectedMateria"
      :selectedMateria="selectedMateria"
      @close-detail="closeDetail"
    />
  </div>
</template>

<script>
import * as d3 from "d3";
import { defineComponent, computed } from "vue";
import { useGraphStore } from "@store/GraphStore";
import GraphFilter from "./GraphFilter.vue";
import GraphMateriaDetalle from "./GraphMateriaDetalle.vue";

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
      selectedMateria: null, // Estado para almacenar la materia seleccionada
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
        await this.store.fetchCycles(filters);
        this.createChart();
      } catch (error) {
        console.error("Error applying filters:", error);
      }
    },
    handlePlanChange(newPlan) {
      this.selectedPlan = newPlan;
      this.fetchSelectedPlan();
    },
    createChart() {
      d3.select(this.$refs.chart).select("svg").remove();

      const width = window.innerWidth;
      const height = window.innerHeight;

      const svg = d3
        .select(this.$refs.chart)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background-color", "#ffffff")
        .on("click", () => this.resetHighlight())
        .call(
          d3.zoom().on("zoom", (event) => {
            g.attr("transform", event.transform);
          })
        );

      const g = svg.append("g");

      svg
        .append("defs")
        .append("marker")
        .attr("id", "arrowhead")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("markerWidth", 8)
        .attr("markerHeight", 8)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#FFD700");

      const nodesByYear = d3.group(this.store.nodes, (d) => d.year);
      const sortedYears = Array.from(nodesByYear.keys()).sort((a, b) =>
        a === "Sin año" ? 1 : b === "Sin año" ? -1 : a - b
      );

      let xOffset = 100;
      const rectGroups = [];
      sortedYears.forEach((year) => {
        const nodes = nodesByYear.get(year) || [];
        let yOffset = 100;
        const rowSpacing = 50;
        const columnSpacing = 200;

        nodes.forEach((node, index) => {
          node.fx = xOffset;
          node.fy = yOffset + index * rowSpacing;
        });

        const yExtent = d3.extent(nodes, (d) => d.fy);

        const rectGroup = g
          .append("g")
          .attr("class", "year-group")
          .call(
            d3.drag().on("drag", (event) => {
              const dx = event.dx;
              const dy = event.dy;
              rectGroup.attr("transform", (d) => {
                const transform =
                  d3.select(rectGroup.node()).attr("transform") || "translate(0,0)";
                const [, tx, ty] =
                  transform.match(/translate\(([-\d.]+),\s*([-\d.]+)\)/) || [
                    null,
                    0,
                    0,
                  ];
                return `translate(${+tx + dx}, ${+ty + dy})`;
              });
              nodes.forEach((node) => {
                node.fx += dx;
                node.fy += dy;
              });
              simulation.alpha(0.3).restart();
            })
          );

        rectGroup
          .append("rect")
          .attr("x", xOffset - 50)
          .attr("y", yExtent[0] - 30)
          .attr("width", columnSpacing)
          .attr("height", yExtent[1] - yExtent[0] + rowSpacing)
          .attr("fill", "rgba(136, 136, 136, 0.1)")
          .attr("stroke", "#888")
          .attr("stroke-width", 2);

        rectGroup
          .append("text")
          .attr("x", xOffset + columnSpacing / 2)
          .attr("y", yExtent[0] - 50)
          .attr("text-anchor", "middle")
          .attr("font-size", "16px")
          .attr("fill", "#636161")
          .text(`Año ${year}`);

        rectGroups.push(rectGroup);
        xOffset += columnSpacing + 100;
      });

      const simulation = d3
        .forceSimulation(this.store.nodes)
        .force(
          "link",
          d3
            .forceLink(this.store.links)
            .id((d) => d.id)
            .distance(150)
        )
        .force("charge", d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(width / 2, height / 2));

      const link = g
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.store.links)
        .enter()
        .append("line")
        .attr("stroke", "#FFD700")
        .attr("stroke-opacity", 0.8)
        .attr("stroke-width", 2)
        .attr("marker-end", "url(#arrowhead)");

      const node = g
        .append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(this.store.nodes)
        .enter()
        .append("circle")
        .attr("r", 20)
        .attr("fill", (d) => d3.schemeTableau10[sortedYears.indexOf(d.year) % 10])
        .call(
          d3
            .drag()
            .on("start", (event, d) => {
              if (!event.active) simulation.alphaTarget(0.3).restart();
              d.fx = d.x;
              d.fy = d.y;
            })
            .on("drag", (event, d) => {
              d.fx = event.x;
              d.fy = event.y;
            })
            .on("end", (event, d) => {
              if (!event.active) simulation.alphaTarget(0);
            })
        )
        .on("click", (event, d) => {
          event.stopPropagation();
          this.highlightConnections(d);
          this.selectedMateria = d;
        });

      const labels = g
        .append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(this.store.nodes)
        .enter()
        .append("text")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")
        .text((d) => d.name)
        .style("font-size", "10px")
        .style("fill", "#5c5a5a")
        .style("pointer-events", "none");

      simulation.on("tick", () => {
        link
          .attr("x1", (d) => d.source.fx)
          .attr("y1", (d) => d.source.fy)
          .attr("x2", (d) => d.target.fx)
          .attr("y2", (d) => d.target.fy);

        node.attr("cx", (d) => d.fx).attr("cy", (d) => d.fy);

        labels.attr("x", (d) => d.fx).attr("y", (d) => d.fy);
      });

      simulation.restart();
    },

    highlightConnections(selectedNode) {
      const connectedNodes = new Set();
      const connectedLinks = new Set();

      this.store.links.forEach((link) => {
        if (link.source.id === selectedNode.id || link.target.id === selectedNode.id) {
          connectedNodes.add(link.source.id);
          connectedNodes.add(link.target.id);
          connectedLinks.add(link);
        }
      });

      // Quitar el borde de todos los nodos
      d3.selectAll(".nodes circle")
        .attr("stroke", null) // Eliminar el borde
        .attr("stroke-width", null)
        .attr("opacity", (d) => (connectedNodes.has(d.id) ? 1 : 0.1));

      // Agregar un borde gris al nodo seleccionado
      d3.selectAll(".nodes circle")
        .filter((d) => d.id === selectedNode.id)
        .attr("stroke", "#bfb9b8") // Color gris
        .attr("stroke-width", 4); // Grosor del borde

      d3.selectAll(".links line")
        .attr("opacity", (d) => (connectedLinks.has(d) ? 1 : 0.1));
    },

    resetHighlight() {
      d3.selectAll(".nodes circle")
        .attr("stroke", null) // Eliminar el borde
        .attr("stroke-width", null)
        .attr("opacity", 1);

      d3.selectAll(".links line")
        .attr("opacity", 1);
    },

    closeDetail() {
      this.selectedMateria = null; // Limpiar la materia seleccionada
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