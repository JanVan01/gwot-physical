function plotTimeseries(rval, t1, t2, tSelector, vSelector) {

  if(!t1[0]){
    $('#demo').text("No data in selected range.");
    return;
  }
    // Setting the box
    var margin = {
            top: 30,
            right: 60,
            bottom: 40,
            left: 60
        },
        width = $(demo).width() - margin.left - margin.right,
        height = $(demo).height() - margin.top - margin.bottom;


    // Define relationship box and axis
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);
    var y1 = d3.scale.linear().range([height, 0]);


    // Define the axes for the data
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(15);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    var yAxis2 = d3.svg.axis().scale(y1)
        .orient("right").ticks(5);



    // Define the line
    var valueline = d3.svg.line()
        .x(function(d) {
            return x(d.datetime);
        })
        .y(function(d) {
            return y(d.value);
        });

    var valueline2 = d3.svg.line()
        .x(function(d) {
            return x(d.datetime);
        })
        .y(function(d) {
            return y1(d.value);
        });


    $('#demo').text("r-Value: " + rval.toFixed(2));
    // Put the area for the graph on the page.
    var svg = d3.select("#demo") // To change to data
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    // Make sure we are dealing with datetime
    t1.forEach(function(d) {
        d.datetime = new Date(d.datetime);
    });

    t2.forEach(function(d) {
        d.datetime = new Date(d.datetime);
    });

    // Scale the range of the data
    var dateMin = Math.min(new Date(t1[0].datetime), new Date(t2[0].datetime));
    var dateMax = Math.max(new Date(t1[t1.length - 1].datetime), new Date(t2[t2.length - 1].datetime));

    console.log("Date: " + new Date(dateMin) + " und " + new Date(dateMax));
    console.log("date min max : " + dateMin + " und " + dateMax);
    var Datedomain = [dateMin, dateMax];
    x.domain(d3.extent(Datedomain, function(d) {
        return d;
    }));
    y.domain([0, d3.max(t1, function(d) {
        return d.value;
    })]);
    y1.domain([0, d3.max(t2, function(d) {
        return d.value;
    })]);

    //Add the valueline path.
    svg.append("path") // Add the valueline path.
        .style("fill", "none")
        .style("stroke", "#000")
        .attr("d", valueline(t1));

    svg.append("path") // Add the valueline2 path.
        .style("stroke", "red")
        .style("fill", "none")
        .style("stroke", "#cc0033")
        .attr("d", valueline2(t2));

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .style("fill", "none")
        .style("stroke", "#000")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .style("fill", "none")
        .style("stroke", "#000")
        .call(yAxis);

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + " ,0)")
        .style("fill", "none")
        .style("stroke", "#cc0033")
        .call(yAxis2);

    svg.append('text')
        .text("")
        .attr('x', 0)
        .attr('y', height + 35);


}
