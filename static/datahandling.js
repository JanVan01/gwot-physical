// Signatur: uncertainty: Array, Array -> Array
// Description: Takes items and associated quality-values, 0 or 1. Returns intervals with a bad quality-value
var uncertainty = function(items, qualities) {
    var result = [];
    var inInterval = null;
    for (var i = 0; i < items.length; i++) {
        if (!inInterval && qualities[i] < 0.5) { // new inIntervalingpoint only when no one was set
            inInterval = items[i];
        }
        if (inInterval && qualities[i] >= 0.5) {
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
    var selected = $("input[type='radio'][name='" + name + "']:checked");
    if (selected.length > 0) {
        selectedVal = selected.val();
    }
    return selectedVal;
}


//Signatur: drawGraph: Number, Number, String, String
//Description: Draws the measurements to a sensor-location - combination for a given timeinterval
function drawGraph(currentSensor, currentLocation, startDate, endDate) {
	var url = 'api/1.0/data/list?limit=10000&sensor=' + currentSensor + '&location=' + currentLocation;
	if (startDate) {
		startDate = moment_fix(parseInt(startDate)).startOf('date').format();
		url += '&start=' + startDate;
	}
	if (endDate) {
		endDate = moment_fix(parseInt(endDate)).endOf('date').format();
		url += '&end=' + endDate;
	}
	if($('#outliers').is(':checked')) {
		url += '&quality=' + $('#outliers').val();
	}
    $.ajax({
        url: url,
        success: function(data, status, ajax) {
            if (data.length === 0) {
                $('#demo').text("Sorry, there is no data available for your selected criteria.");
                return;
            } else {
                var dateTime = ['time'];
                var measurements = ['measurements'];
                var measurementQuality = [];
                var unit = data[0].sensor.unit;
                for (i = 0; i < data.length; i++) {
                    dateTime.push(moment_fix(data[i].datetime).format());
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
                                format: '%Y-%m-%d %H:%M',
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
            }
        },
        error: function(ajax, status, error) {
			$('#demo').text("Sorry, can't load data from device.");
        },
        dataType: "json",
        headers: {
            accept: 'application/json'
        }
    });

}


//Signatur: filtersChanged: Number
//Action performed if a selection is changed
function filtersChanged() {
    var currentSensor = getSelectedButtonValue('sensor');
    var currentLocation = getSelectedButtonValue('location');
    try {
        var i = slider.noUiSlider.get();
        drawGraph(currentSensor, currentLocation, i[0], i[1]);
    } catch (err) {
        drawGraph(currentSensor, currentLocation);
    }
}

// Create a string representation of the date.
function formatDate(date) {
	return moment_fix(date).format('YYYY-MM-DD')
}


function moment_fix(time) {
	return moment(time).utc().add(new Date().getTimezoneOffset(), 'minutes');
}

//Signatur: drawBar: String
//Description: Draws a Date-Slider to a given max-Date (String). Min-Value is 2016-06-01
function drawBar() {
    var dateSlider = document.getElementById('slider');
	var min_datetime = moment_fix(timerange.min).startOf('date').valueOf();
	var max_datetime = moment_fix(timerange.max).endOf('date').valueOf();
	var seconds_per_day = 24 * 60 * 60 * 1000;
	var start = max_datetime - seconds_per_day * 7;
	if (min_datetime > start) {
		start = min_datetime;
	}
    noUiSlider.create(dateSlider, {
        // Create two timestamps to define a range.
        range: {
            min: min_datetime,
            max: max_datetime
        },
        // Steps of one day
        step: seconds_per_day,
        // Two more timestamps indicate the handle starting positions.
        start: [start, max_datetime],
        // No decimals
        format: wNumb({
            decimals: 0
        })
    });



		// For updating labeling of the Date-Slider
    var dateValues = [
        document.getElementById('eventStart'),
        document.getElementById('eventEnd')
    ];

    //updating the shown date
    dateSlider.noUiSlider.on('update', function(values, handle) {
        dateValues[handle].innerHTML = formatDate(new Date(+values[handle]));
    });

    //Action if the slide stops
    dateSlider.noUiSlider.on('end', function(values, handle) {
        var currentSensorId = getSelectedButtonValue('sensor');
        var currentLocationId = getSelectedButtonValue('location');
        drawGraph(currentSensorId, currentLocationId, values[0], values[1])
    });
}
