// Signatur: uncertainty: Array, Array -> Array
// Description: Takes items and associated quality-values, 0 or 1. Returns intervals with a bad quality-value
var uncertainty = function (items, qualities) {
	var result = [];
	var inInterval = null;
	for (var i = 0; i < items.length; i++) {
		if (!inInterval && qualities[i] == 0) { // new inIntervalingpoint only when no one was set
			inInterval = items[i];
		}
		if (inInterval && qualities[i] == 1) {
			result.push({
				start: inInterval,
				end: items[i]
			})
			inInterval = null; // measurement with good quality seen, so close the interval
		}
	}
	return result;
}

// Signatur: getSelectedButtonValue: String -> int
// Description: Returns the selected value of a set of radio buttons grouped by name.
function getSelectedButtonValue(name) {
	var selectedVal = 0;
	var selected = $("input[type='radio'][name='"+name+"']:checked");
	if (selected.length > 0) {
		selectedVal = selected.val();
	}
	return selectedVal;
}


function drawGraph(currentSensor, currentLocation) {
	$.ajax({
		url: 'api/1.0/data/list?sensor=' + currentSensor + '&location=' + currentLocation,
		success: function (data, status, ajax) {
			if (data.length === 0) {
				$('#demo').text("Sorry, no data delivered by server.");
				return;
			}
			var dateTime = ['time'];
			var measurements = ['measurements'];
			var measurementQuality = [];
			var unit = data[0].sensor.unit;
			for (i = 0; i < data.length; i++) {
				dateTime.push(data[i].datetime);
				measurements.push(data[i].value);
				measurementQuality.push(data[i].quality);
			}
			var chart = c3.generate({
				bindto: '#demo',
				data: {
					x: 'time',
					columns: [
						measurements,
						dateTime
					]
				},
				zoom: {
					enabled: true
				},
				axis: {
					x: {
						type: 'timeseries',
						tick: {
							format: '%Y-%m-%d %H-%M',
							count: 1 + Math.ceil(dateTime.length / (dateTime.length / 4))
						}
					},
					y: {
						label: unit
					},
				},
				subchart: {
					show: true,
					size: {
						height: 75
					},
				},
				regions: uncertainty(dateTime, measurementQuality)
			});
		},
		error: function (ajax, status, error) {
			$('#demo').text("Sorry, can't load data.");
		},
		dataType: "json",
		headers: {
			accept: 'application/json'
		}
	});
}

function sensorChanged(id) {
	var currentLocation = getSelectedButtonValue('location')
	drawGraph(id, currentLocation);
}

function locationChanged(id) {
	var currentSensor = getSelectedButtonValue('sensor');
	drawGraph(currentSensor, id);
}

$(function() {
	$('[data-toggle="tooltip"]').tooltip();
	$("input:radio[name=sensor]:first").attr('checked', true).trigger('change');
	$("input:radio[name=location]:first").attr('checked', true).trigger('change');
});