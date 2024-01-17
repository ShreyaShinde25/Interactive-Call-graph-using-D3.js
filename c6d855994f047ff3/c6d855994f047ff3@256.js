import define1 from "./a33468b95d0b15b0@817.js";

function _1(md){

// md`<div style="color: grey; font: 13px/25.5px var(--sans-serif); text-transform: uppercase;"><h1 style="display: none;">Mobile patent suits</h1><a href="https://d3js.org/">D3</a> › <a href="/@d3/gallery">Gallery</a></div>

// # Mobile patent suits

// A view of patent-related lawsuits in the mobile communications industry, circa 2011. Data: [Thomson Reuters](http://blog.thomsonreuters.com/index.php/mobile-patent-suits-graphic-of-the-day/)`
}

function _2(Swatches,chart){return(
Swatches(chart.scales.color)
)}

function _chart(suits,d3,location,drag,linkArc,invalidation)
{

  const width = 928;
  const height = 600;
  const types = Array.from(new Set(suits.map(d => d.type)));
  const nodes = Array.from(new Set(suits.flatMap(l => [l.source, l.target])), id => ({id}));
  const links = suits.map(d => Object.create(d))

  const color = d3.scaleOrdinal(types, d3.schemeCategory10)

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-400))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

  const svg = d3.create("svg")
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("width", width)
      .attr("height", height)
      .attr("style", "max-width: 100%; height: auto; font: 12px sans-serif;");
  
  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
    .data(types)
    .join("marker")
      .attr("id", d => `arrow-${d}`)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -0.5)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
    .append("path")
      .attr("fill", color)
      .attr("d", "M0,-5L10,0L0,5");

  const link = svg.append("g")
      .attr("fill", "none")
      .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(links)
    .join("path")
      .attr("stroke", d => color(d.type))
      .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

  const node = svg.append("g")
      .attr("fill", "currentColor")
      .attr("stroke-linecap", "round")
      .attr("stroke-linejoin", "round")
    .selectAll("g")
    .data(nodes)
    .join("g")
      .call(drag(simulation));

  node.append("circle")
      .attr("stroke", "white")
      .attr("stroke-width", 1.5)
      .attr("r", 4);

  node.append("text")
      .attr("x", 8)
      .attr("y", "0.31em")
      .text(d => d.id)
    .clone(true).lower()
      .attr("fill", "none")
      .attr("stroke", "white")
      .attr("stroke-width", 3);

  simulation.on("tick", () => {
    link.attr("d", linkArc);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  invalidation.then(() => simulation.stop());

  return Object.assign(svg.node(), {scales: {color}});
}


function _suits(FileAttachment){return(
FileAttachment("caller_callee_relationship@1.csv").csv()
)}

function _linkArc(){return(
function linkArc(d) {
  const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
  return `
    M${d.source.x},${d.source.y}
    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
  `;
}
)}

function _drag(d3){return(
simulation => {
  
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }
  
  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  
  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}
)}

function _caller_callee_relationship(__query,FileAttachment,invalidation){return(
__query(FileAttachment("caller_callee_relationship.csv"),{from:{table:"caller_callee_relationship"},sort:[],slice:{to:null,from:null},filter:[],select:{columns:null}},invalidation)
)}

export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["caller_callee_relationship.csv", {url: new URL("./files/be6cb7afdc1a9fbb93748180bc9bcdd9fd5238614a1c53437a4e61df097096570bfbc1a4c59dd054e2c8513beab0f55bce7ddc2710677f03c7f10f6efa63c0a2.csv", import.meta.url), mimeType: "text/csv", toString}],
    ["caller_callee_relationship@1.csv", {url: new URL("./files/be6cb7afdc1a9fbb93748180bc9bcdd9fd5238614a1c53437a4e61df097096570bfbc1a4c59dd054e2c8513beab0f55bce7ddc2710677f03c7f10f6efa63c0a2.csv", import.meta.url), mimeType: "text/csv", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  //main.variable(observer()).define(["md"], _1);
  main.variable(observer()).define(["Swatches","chart"], _2);
  main.variable(observer("chart")).define("chart", ["suits","d3","location","drag","linkArc","invalidation"], _chart);
  main.variable().define("suits", ["FileAttachment"], _suits);
  main.variable().define("linkArc", _linkArc);
  main.variable().define("drag", ["d3"], _drag);
  const child1 = runtime.module(define1);
  main.import("Swatches", child1);
  main.variable().define("caller_callee_relationship", ["__query","FileAttachment","invalidation"], _caller_callee_relationship);
  return main;
}
