function updateData (current_id) {
	$("#title_sensor").text(sensordata[current_id].sensor.type);
	$("#unit").text(sensordata[current_id].sensor.unit);
	$("#min_values").html("<th>Minimum</th>" +
			"<td>" + sensordata[current_id].daily.min + "</td>"
			+ "<td>" + sensordata[current_id].hourly.min + "</td>"
			+ "<td>" + sensordata[current_id].monthly.min + "</td>"
			+ "<td>" + sensordata[current_id].yearly.min + "</td>"
			+ "<td>" + sensordata[current_id].accum.min + "</td>");
	$("#avg_values").html("<th>Average</th>" +
			"<td>" + sensordata[current_id].daily.avg + "</td>"
			+ "<td>" + sensordata[current_id].hourly.avg + "</td>"
			+ "<td>" + sensordata[current_id].monthly.avg + "</td>"
			+ "<td>" + sensordata[current_id].yearly.avg + "</td>"
			+ "<td>" + sensordata[current_id].accum.avg + "</td>");
	$("#max_values").html("<th>Maximum</th>" +
			"<td>" + sensordata[current_id].daily.max + "</td>"
			+ "<td>" + sensordata[current_id].hourly.max + "</td>"
			+ "<td>" + sensordata[current_id].monthly.max + "</td>"
			+ "<td>" + sensordata[current_id].yearly.max + "</td>"
			+ "<td>" + sensordata[current_id].accum.max + "</td>");

	$("#last_time").text(sensordata[current_id].datetime);
	$("#trend").text(sensordata[current_id].trend);
	$("#curr_time").html("<i>Page generated on " + Date().slice(0,-9) + "</i>");
	
	if (sensordata[current_id].last === 'None') {
		$("#last_box").hide();
		return;
	}

	$("#last_box").show();
	
	var pretty = (sensordata[current_id].sensor.type == 'HC-SR04'); // Not nice tosolve it like this, but in this usecase ...
	var min = pretty ? 0 : sensordata[current_id].accum.min;
	var max = pretty ? loc_height : sensordata[current_id].accum.max;
	var options = {
		bindto: '#last_value',
		data: {
			columns: [['data', sensordata[current_id].last]],
			type: 'gauge'
		},
		gauge: {
			label:{
				format: function(value, ratio){ return value; }
			},
			min: min,
			max: max,
			units: sensordata[current_id].sensor.unit
		},
	};
	if (pretty) {
		options.color = {
			pattern: ['#60B044', '#F6C600', '#FF0000'],
			threshold: {
				unit: 'value',
				max: max,
				values: [max*0.5, max*0.8, max]
			}
		};
	}
	c3.generate(options);
}

function createmap(lon, lat) {
	var mymap = L.map('map').setView([lon, lat], 18);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
	maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
			id: 'mapbox.streets'
	}).addTo(mymap);
	L.marker([lon, lat]).addTo(mymap);
}