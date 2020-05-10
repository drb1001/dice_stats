
const svg_dims = {width: 900, height: 500};
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

Promise.all([
    d3.json(d1_url),
    d3.json(d2_url)
])
.then(([d1_data, d2_data]) =>  {
    console.log(d1_data);
    console.log(d2_data);

    const d1_data_rolls = d1_data.rolls;
    const d1_data_stats = d1_data.stats;
    const d2_data_rolls = d2_data.rolls;
    const d2_data_stats = d2_data.stats;

    const data_comb = d1_data_rolls.concat(d2_data_rolls);
    const max_pip_total = _.max(data_comb.map(d => d.pip_total));
    const max_prob = _.max(data_comb.map(d => d.probability));

    x_scale.domain([0,max_pip_total]);
    y_scale.domain([0, max_prob*1.1]).nice();

    const x_scale_padding = 20;
    const x_width = Math.max(1, (x_scale(1) - x_scale_padding)/2);

    // Draw ares chart for d1
    g.append("path")
      .datum(d1_data_rolls)
      .attr("fill", "red")
      .attr("fill-opacity", 0.7)
      .attr("d", d3.area()
         .x(d => x_scale(d.pip_total))
         .y0(y_scale(0))
         .y1(d => y_scale(d.probability))
      );

    // Draw ares chart for d2
    g.append("path")
      .datum(d2_data_rolls)
      .attr("fill", "green")
      .attr("fill-opacity", 0.7)
      .attr("d", d3.area()
         .x(d => x_scale(d.pip_total))
         .y0(y_scale(0))
         .y1(d => y_scale(d.probability))
      );

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


    console.log([d1_data_stats, d2_data_stats]);

    // Update the table
    var table = d3.select("#stats_table_body")
       .selectAll("tr")
       .data([d1_data_stats, d2_data_stats])
       .enter().append("tr");

    var td = table.selectAll("td")
      .data(function(d, i) { return Object.values(d); })
      .enter().append("td")
        .text(function(d) { return d; });

})
.catch(function(error){
   // handle error


})
