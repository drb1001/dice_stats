
const svg_dims = {width: 960, height: 500};
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const width = svg_dims.width - margin.left - margin.right;
const height = svg_dims.height - margin.top - margin.bottom;

const svg = d3.select('svg')
    .attr("width", svg_dims.width)
    .attr("height", svg_dims.height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    .attr("id", "chart");

const g = d3.select('#chart');


var x_scale = d3.scaleLinear()
    .rangeRound([0, width]);


const x_padding = 0.1;

var y_scale = d3.scaleLinear()
    .rangeRound([height, 0]);


const d1 = d3.select('#d1Input').property('value');
const d2 = d3.select('#d2Input').property('value');

const d1_url = '/get_data?d=' + encodeURIComponent(d1);
const d2_url = '/get_data?d=' + encodeURIComponent(d2);

const legend_data = [{d: 'd1', value: d1, color: 'green'},
                      {d: 'd2', value: d2, color: 'red'}]

console.log(d1);
console.log(d2);
console.log(d1_url);
console.log(d2_url);

Promise.all([
    d3.json(d1_url),
    d3.json(d2_url)
])
.then(([d1_data, d2_data]) =>  {
    console.log(d1_data);
    console.log(d2_data);

    const data_comb = d1_data.concat(d2_data);
    const max_pip_total = _.max(data_comb.map(d => d.pip_total));
    const max_prob = _.max(data_comb.map(d => d.probability));

    console.log(max_pip_total);
    console.log(max_prob);

    x_scale.domain([0,max_pip_total]);
    y_scale.domain([0, max_prob]).nice();

    const x_scale_padding = 20;
    const x_width = Math.max(1, (x_scale(1) - x_scale_padding)/2);

    console.log('ok');

    // Draw data for d1
    g.append("g")
      .selectAll("rect")
      .data(d1_data)
      .enter().append("rect")
      .attr("class", "d1_rect")
      .attr("x", d => x_scale(d.pip_total) - x_width)
      .attr("y", d => y_scale(d.probability))
      .attr("width", x_width)
      .attr("height", d => (height - y_scale(d.probability)))
      .attr("fill", _.filter(legend_data, e => e.d == 'd1')[0].color);
      // .attr("transform", function(d) { return "translate(" + x0(d.State) + ",0)"; })

      // Draw data for d2
      g.append("g")
        .selectAll("rect")
        .data(d2_data)
        .enter().append("rect")
        .attr("class", "d2_rect")
        .attr("x", d => x_scale(d.pip_total))
        .attr("y", d => y_scale(d.probability))
        .attr("width", x_width)
        .attr("height", d => (height - y_scale(d.probability)))
        .attr("fill", _.filter(legend_data, e => e.d == 'd2')[0].color);
        // .attr("transform", function(d) { return "translate(" + x0(d.State) + ",0)"; })

      // Draw x-axis
      g.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x_scale));

      // Draw legend
      var legend = g.append("g")
        .attr("class", "legend");

      legend.selectAll("text")
         .data(legend_data)
         .enter().append("text")
         .attr("class", "legend_text")
         .attr("fill", d => d.color)
         .text(d => d.value)
         .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });


})
.catch(function(error){
   // handle error


})
