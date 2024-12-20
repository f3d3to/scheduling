<template>
  <div>
    <select v-model="selectedPlan" @change="fetchSelectedPlan">
      <option v-for="plan in plans" :key="plan.id" :value="plan.id">
        {{ plan.nombre }}
      </option>
    </select>
    <div ref="chart"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { fetchPlans, fetchCycles } from "../services/apiService";

export default {
  name: "GraphContainer",
  data() {
    return {
      plans: [],
      selectedPlan: null,
      nodes: [],
      links: [],
    };
  },
  async mounted() {
    try {
      const plansData = await fetchPlans();
      this.plans = plansData.results;
      if (this.plans.length > 0) {
        this.selectedPlan = this.plans[0].id;
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
        const data = await fetchCycles(this.selectedPlan);
        this.processData(data.anios);
        this.createChart();
      } catch (error) {
        console.error("Error fetching plan cycles:", error);
      }
    },
    processData(anios) {
      const nodes = [];
      const links = [];
      const nodeMap = new Map();

      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          materias.forEach((materia) => {
            const node = {
              id: materia.codigo.trim(),
              name: materia.nombre.trim(),
              year: key === "0" ? "Sin año" : parseInt(key, 10),
            };
            nodes.push(node);
            nodeMap.set(materia.codigo.trim(), node);
          });
        }
      });

      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          materias.forEach((materia) => {
            if (materia.correlativas && Array.isArray(materia.correlativas)) {
              materia.correlativas.forEach((correlativa) => {
                const trimmedCorrelativa = correlativa.trim();
                if (nodeMap.has(trimmedCorrelativa)) {
                  links.push({
                    source: trimmedCorrelativa,
                    target: materia.codigo.trim(),
                  });
                } else {
                  console.warn(`Correlativa ${trimmedCorrelativa} no encontrada en los nodos.`);
                }
              });
            }
          });
        }
      });

      this.nodes = nodes;
      this.links = links;
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
        .style("background-color", "#1E1E1E")
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

      const nodesByYear = d3.group(this.nodes, (d) => d.year);
      const sortedYears = Array.from(nodesByYear.keys()).sort((a, b) => (a === "Sin año" ? 1 : b === "Sin año" ? -1 : a - b));

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
                const transform = d3.select(rectGroup.node()).attr("transform") || "translate(0,0)";
                const [, tx, ty] = transform.match(/translate\(([-\d.]+),\s*([-\d.]+)\)/) || [null, 0, 0];
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
          .attr("fill", "#fff")
          .text(`Año ${year}`);

        rectGroups.push(rectGroup);
        xOffset += columnSpacing + 100;
      });

      const simulation = d3
        .forceSimulation(this.nodes)
        .force(
          "link",
          d3
            .forceLink(this.links)
            .id((d) => d.id)
            .distance(150)
        )
        .force("charge", d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(width / 2, height / 2));

      const link = g
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.links)
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
        .data(this.nodes)
        .enter()
        .append("circle")
        .attr("r", 20)
        .attr("fill", (d) => d3.schemeTableau10[sortedYears.indexOf(d.year) % 10])
        .call(
          d3.drag()
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
        });

      const labels = g
        .append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(this.nodes)
        .enter()
        .append("text")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")
        .text((d) => d.name)
        .style("font-size", "10px")
        .style("fill", "#FFFFFF")
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

      this.links.forEach((link) => {
        if (link.source.id === selectedNode.id || link.target.id === selectedNode.id) {
          connectedNodes.add(link.source.id);
          connectedNodes.add(link.target.id);
          connectedLinks.add(link);
        }
      });

      d3.selectAll(".nodes circle")
        .attr("opacity", (d) => (connectedNodes.has(d.id) ? 1 : 0.1));

      d3.selectAll(".links line")
        .attr("opacity", (d) => (connectedLinks.has(d) ? 1 : 0.1));
    },
    resetHighlight() {
      d3.selectAll(".nodes circle").attr("opacity", 1);
      d3.selectAll(".links line").attr("opacity", 1);
    },
  },
};
</script>

<style scoped>
svg {
  width: 100%;
  height: 100%;
  background-color: #1e1e1e;
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
