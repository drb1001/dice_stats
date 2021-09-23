
function create_chart(d_values) {

  console.log(d_values);

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


  Promise.all(d_values.map(
    id => fetch('/get_data?d=' + encodeURIComponent(id)).then(resp => resp)
  ))
  .then(function(result){
    return Promise.all(result.map(v => v.json().then(function(r) { return {"ok": v.ok, "json": r} }) ))
  })
  .catch(function(error){
    console.log("ERROR");
    console.log(error);
  })
  .then(function(data){

    // Work out the chart axis scales
    console.log(data);
    const data_comb = data.map(function(e){
        if(typeof e.json === 'object' && e.json.hasOwnProperty('rolls')){
          return e.json.rolls
        } else {
          return new Object
        }
    }).flat();
    const max_pip_total = (_.max(_.mapObject(data_comb, d => d.pip_total)));
    const max_prob = (_.max(_.mapObject(data_comb, d => d.probability)));
    console.log('max_pip_total', max_pip_total, 'max_prob', max_prob);

    x_scale.domain([0,max_pip_total]);
    y_scale.domain([0, max_prob]).nice();

    const x_scale_padding = 20;
    const x_width = Math.max(1, (x_scale(1) - x_scale_padding)/2);

    var draw_axes = false;

    // Handle case when API returns with bad data or error
    data.forEach(function(el, ix){

        if (!el.ok) {
          console.log(el);
          const chart_div = d3.select('.jumbotron');
          chart_div.append("p")
            .attr("class", "error_msg")
            .text(data[ix].json)
            .style("color", "red");

        } else {

          draw_axes = true;

          console.log(el.json);
          const data_rolls = el.json.rolls;
          const data_stats = el.json.stats;

          // Draw area chart
          g.append("path")
            .datum(data_rolls)
            .attr("fill", colorScale(ix))
            .attr("fill-opacity", 0.6)
            .attr("d", d3.area()
               .x(d => x_scale(d.pip_total))
               .y0(y_scale(0))
               .y1(d => y_scale(d.probability))
            );

          // Draw line chart
          svg.append("path")
            .datum(data_rolls)
            .attr("fill", "none")
            .attr("stroke", colorScale(ix))
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
              .x(d => x_scale(d.pip_total))
              .y(d => y_scale(d.probability))
            );

          // Add stats to the table
          var table = d3.select("#stats_table_body")
             .append("tr")
             .style("color", colorScale(ix))
             .html(`<td>${data_stats['name']}</td><td>${data_stats['avg']}</td><td>${data_stats['mode']}</td><td>${data_stats['pct80_range']}</td><td>${data_stats['max_range']}</td>`);

        }
      });

      // Draw x-axis
      if(draw_axes) {
        g.append("g")
          .attr("class", "x-axis")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x_scale));
      }

  })
  .catch(function(error){
    console.log("ERROR");
    console.log(error);
  })
}


const d_values = ['#d1Input', '#d2Input', '#d3Input'].map(
  el => d3.select(el).property('value')
).filter(
  el => el
);

create_chart(d_values);
