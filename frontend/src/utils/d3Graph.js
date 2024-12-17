import * as d3 from "d3";

export function createSVGContainer(ref, width, height) {
  const svg = d3
    .select(ref)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .style("background-color", "#1E1E1E");

  // Agregar un grupo para contener los elementos gráficos
  const g = svg.append("g");

  // Configurar el zoom y vincularlo al grupo `g`
  svg.call(
    d3.zoom().on("zoom", (event) => {
      g.attr("transform", event.transform);
    })
  );

  return g; // Devolver el grupo `g` donde se dibujarán los nodos y enlaces
}

export function createForceSimulation(nodes, links) {
  return d3
    .forceSimulation(nodes)
    .force("link", d3.forceLink(links).id((d) => d.id).distance(150))
    .force("charge", d3.forceManyBody().strength(-50))
    .force("center", d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2));
}

export function drawLinks(svg, links) {
  svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .attr("stroke", "#FFD700")
    .attr("stroke-width", 2)
    .attr("marker-end", "url(#arrowhead)");
}

export function drawNodes(svg, nodes, onClickCallback) {
  svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", 20)
    .attr("fill", (d) => d3.schemeTableau10[d.year % 10])
    .on("click", (event, d) => onClickCallback(d.id));
}
