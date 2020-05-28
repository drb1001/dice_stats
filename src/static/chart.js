
function create_chart(d1_url, d2_url) {

  var svg_width = d3.select('.chart').node().getBoundingClientRect().width;
  const svg_dims = {width: svg_width, height: svg_width*0.5};

  const margin = {top: 5, right: 10, bottom: 20, left: 10};
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

  var y_scale = d3.scaleLinear()
      .rangeRound([height, 0]);

  var colorScale = d3.scaleOrdinal(d3.schemeSet1);

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
      y_scale.domain([0, max_prob]).nice();

      const x_scale_padding = 20;
      const x_width = Math.max(1, (x_scale(1) - x_scale_padding)/2);

      // Draw area chart for d1
      g.append("path")
        .datum(d1_data_rolls)
        .attr("fill", colorScale(0))
        .attr("fill-opacity", 0.7)
        .attr("d", d3.area()
           .x(d => x_scale(d.pip_total))
           .y1(d => y_scale(d.probability))
           .y0(y_scale(0))
        );

      // Draw line chart for d1
      svg.append("path")
        .datum(d1_data_rolls)
        .attr("fill", "none")
        .attr("stroke", colorScale(0))
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
          .x(d => x_scale(d.pip_total))
          .y(d => y_scale(d.probability))
        );

      // Draw area charts for d2
      g.append("path")
        .datum(d2_data_rolls)
        .attr("fill", colorScale(1))
        .attr("fill-opacity", 0.7)
        .attr("d", d3.area()
           .x(d => x_scale(d.pip_total))
           .y0(y_scale(0))
           .y1(d => y_scale(d.probability))
        );

      // Draw line chart for d2
      svg.append("path")
        .datum(d2_data_rolls)
        .attr("fill", "none")
        .attr("stroke", colorScale(1))
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
          .x(d => x_scale(d.pip_total))
          .y(d => y_scale(d.probability))
        );

      // Draw x-axis
      g.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x_scale));

      // Update the table
      var table = d3.select("#stats_table_body")
         .selectAll("tr")
         .data([d1_data_stats, d2_data_stats])
         .enter().append("tr")
         .style("color", function(d,i){return colorScale(i);});

      var td = table.selectAll("td")
        .data(function(d, i) { return [d['name'], d['avg'], d['mode'], d['pct80_range'], d['max_range']] })
        .enter().append("td")
        .text(function(d) { return d; });

  })
  .catch(function(error){
     // handle error
     const chart_div = d3.select('main');
     chart_div.append("p").lower()
        .attr("class", "error_msg")
        .text("Unknown dice roll")
        .style("color", "red");

  })
}



const d1 = d3.select('#d1Input').property('value');
const d2 = d3.select('#d2Input').property('value');

if (d1 && d2) {
  const d1_url = '/get_data?d=' + encodeURIComponent(d1);
  const d2_url = '/get_data?d=' + encodeURIComponent(d2);
  create_chart(d1_url, d2_url);
}
