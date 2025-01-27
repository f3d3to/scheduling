// graphUtils.js
import * as d3 from "d3";

export const createChart = (containerRef, nodes, links, promocionadas, highlightConnections, resetHighlight) => {
  d3.select(containerRef).select("svg").remove();

  const width = window.innerWidth;
  const height = window.innerHeight;

  const svg = d3
    .select(containerRef)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .style("background-color", "#ffffff")
    .on("click", () => resetHighlight())
    .call(
      d3.zoom().on("zoom", (event) => {
        g.attr("transform", event.transform);
      })
    );

  const g = svg.append("g");

  // Crear marcadores dinámicos basados en colores únicos
  const uniqueColors = [...new Set(links.map(link => link.color || '#FFD700'))];
  uniqueColors.forEach(color => {
    svg
      .append("defs")
      .append("marker")
      .attr("id", `arrowhead-${color.replace('#', '')}`)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", 0)
      .attr("markerWidth", 8)
      .attr("markerHeight", 8)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", color);
  });

  const nodesByYear = d3.group(nodes, (d) => d.year);
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
      .attr("x", xOffset - 80)
      .attr("y", yExtent[0] - 25)
      .attr("width", columnSpacing)
      .attr("height", yExtent[1] - yExtent[0] + rowSpacing)
      .attr("fill", "rgba(136, 136, 136, 0.1)")
      .attr("stroke", "#888")
      .attr("stroke-width", 2);

    rectGroup
      .append("text")
      .attr("x", xOffset + columnSpacing  / 2 - 90)
      .attr("y", yExtent[0] - 50)
      .attr("text-anchor", "middle")
      .attr("font-size", "16px")
      .attr("fill", "#636161")
      .text(`Año ${year}`);

    rectGroups.push(rectGroup);
    xOffset += columnSpacing + 100;
  });

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(150)
    )
    .force("charge", d3.forceManyBody().strength(-50))
    .force("center", d3.forceCenter(width / 2, height / 2));

  // Enlaces (usar color del backend)
  const link = g
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .attr("stroke", (d) => d.color || '#FFD700') // Color del backend
    .attr("stroke-opacity", 0.8)
    .attr("stroke-width", 2)
    .attr("marker-end", (d) => `url(#arrowhead-${(d.color || '#FFD700').replace('#', '')})`); // Marcador dinámico
  // Nodos (usar color del backend)
  const node = g
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", 20)
    .attr("fill", (d) => d.customColor || d.color || '#4CAF50')
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
      highlightConnections(d);
    });

  // Etiquetas de los nodos
  const labels = g
    .append("g")
    .attr("class", "labels")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .text((d) => d.name)
    .style("font-size", "12px")
    .style("fill", "#5c5a5a") // Texto blanco
    .style("stroke", "rgba(255, 255, 255, 0.7)") // Contorno negro semi-transparente
    .style("stroke-width", 2)
    .style("paint-order", "stroke") // Renderiza primero el contorno
    .style("text-decoration", (d) => ((promocionadas && d.materiaEstudiante?.estado === 'promocionada') ? 'line-through' : 'none')) // Tachar nombres de aprobadas
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
};

export const highlightConnections = (selectedNode, nodes, links) => {
  const connectedNodes = new Set();
  const connectedLinks = new Set();

  links.forEach((link) => {
    if (link.source.id === selectedNode.id || link.target.id === selectedNode.id) {
      connectedNodes.add(link.source.id);
      connectedNodes.add(link.target.id);
      connectedLinks.add(link);
    }
  });

  // Quitar el borde de todos los nodos
  d3.selectAll(".nodes circle")
    .attr("stroke", null)
    .attr("stroke-width", null)
    .attr("opacity", (d) => (connectedNodes.has(d.id) ? 1 : 0.1));

  // Agregar un borde gris al nodo seleccionado
  d3.selectAll(".nodes circle")
    .filter((d) => d.id === selectedNode.id)
    .attr("stroke", "#bfb9b8")
    .attr("stroke-width", 4);

  d3.selectAll(".links line")
    .attr("opacity", (d) => (connectedLinks.has(d) ? 1 : 0.1));
};

export const resetHighlight = () => {
  d3.selectAll(".nodes circle")
    .attr("stroke", null)
    .attr("stroke-width", null)
    .attr("opacity", 1);

  d3.selectAll(".links line")
    .attr("opacity", 1);
};