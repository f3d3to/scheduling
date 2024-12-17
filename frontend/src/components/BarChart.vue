<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "GraphContainer",
  data() {
    return {
      nodes: [],
      links: [],
    };
  },
  async mounted() {
    await this.fetchData();
    this.createChart();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("http://localhost:8000/planes/1/ciclos/");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        const anios = data.anios;

        if (!anios || typeof anios !== "object" || Array.isArray(anios)) {
          throw new Error(
            "'anios' field must be a non-array object. Verify backend response."
          );
        }

        this.processData(anios);
      } catch (error) {
        console.error("Error fetching data:", error);
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
              year: parseInt(key),
            };
            nodes.push(node);
            nodeMap.set(materia.codigo.trim(), node);
          });
        }
      });

      Object.entries(anios).forEach(([key, materias]) => {
        if (Array.isArray(materias)) {
          materias.forEach((materia) => {
            console.log("Processing materia:", materia);
            if (materia.correlativas && Array.isArray(materia.correlativas)) {
              materia.correlativas.forEach((correlativa) => {
                const trimmedCorrelativa = correlativa.trim();
                if (nodeMap.has(trimmedCorrelativa)) {
                  links.push({
                    source: trimmedCorrelativa, // Swap source and target to fix arrow direction
                    target: materia.codigo.trim(),
                  });
                } else {
                  console.warn(
                    `Correlativa ${trimmedCorrelativa} not found in nodes.`
                  );
                }
              });
            }
          });
        }
      });

      console.log("Nodes:", nodes);
      console.log("Links:", links);

      this.nodes = nodes;
      this.links = links;
    },
    async fetchCorrelatives(nodeId) {
      try {
        const response = await fetch(`http://localhost:8000/materias/${nodeId}/correlativas/`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const correlatives = await response.json();

        console.log("Fetched correlatives (raw):", correlatives);

        let flatCorrelatives = [];
        if (Array.isArray(correlatives)) {
          flatCorrelatives = correlatives.flatMap((item) => item.correlativas || []);
        } else if (correlatives.correlativas) {
          flatCorrelatives = correlatives.correlativas;
        } else {
          console.warn("Unrecognized correlatives structure:", correlatives);
        }

        console.log("Processed correlatives:", flatCorrelatives);

        if (flatCorrelatives.length > 0) {
          return flatCorrelatives;
        } else {
          console.warn("No correlatives found or invalid response format.");
          return [];
        }
      } catch (error) {
        console.error("Error fetching correlatives:", error);
        return [];
      }
    },
    createChart() {
      const width = window.innerWidth;
      const height = window.innerHeight;

      const svg = d3
        .select(this.$refs.chart)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background-color", "#1E1E1E")
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

      let xOffset = 100;
      nodesByYear.forEach((nodes, year) => {
        let yOffset = 100;
        const rowSpacing = 50;
        const columnSpacing = 200;

        nodes.forEach((node, index) => {
          node.fx = xOffset;
          node.fy = yOffset + index * rowSpacing;
        });

        const yExtent = d3.extent(nodes, (d) => d.fy);

        g.append("rect")
          .attr("x", xOffset - 50)
          .attr("y", yExtent[0] - 30)
          .attr("width", columnSpacing)
          .attr("height", yExtent[1] - yExtent[0] + rowSpacing)
          .attr("fill", "rgba(136, 136, 136, 0.1)")
          .attr("stroke", "#888")
          .attr("stroke-width", 2)
          .attr("class", `year-group year-${year}`);

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
        .force("charge", d3.forceManyBody().strength(0))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .stop();

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
        .attr("fill", (d) => d3.schemeTableau10[d.year % 10])
        .attr("id", (d) => d.id)
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
        .on("click", async (event, d) => {
          d3.selectAll("circle").attr("opacity", 0.1);
          d3.selectAll("line").attr("opacity", 0.1);

          d3.select(event.target)
            .attr("opacity", 1)
            .transition()
            .attr("stroke", "yellow")
            .attr("stroke-width", 3);

          const correlatives = await this.fetchCorrelatives(d.id);

          console.log("Clicked node correlatives:", correlatives);

          if (correlatives.length > 0) {
            correlatives.forEach((correlative) => {
              d3.select(`circle[id='${correlative}']`).attr("opacity", 1);
              link.each(function (l) {
                if (
                  (l.source.id === d.id && l.target.id === correlative) ||
                  (l.target.id === d.id && l.source.id === correlative)
                ) {
                  d3.select(this).attr("opacity", 1);
                }
              });
            });
          } else {
            console.warn("No correlatives found or invalid response format.");
          }
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
