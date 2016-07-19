// Signatur: uncertainty: Array, Array -> Array
// Description: Takes items and associated quality-values, 0 or 1. Returns intervals with a bad quality-value
var uncertainty = function(items, qualities) {
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
    var selected = $("input[type='radio'][name='" + name + "']:checked");
    if (selected.length > 0) {
        selectedVal = selected.val();
    }
    return selectedVal;
}


//Signatur: drawGraph: Number, Number, String, String
//Description: Draws the measurements to a sensor-location - combination for a given timeinterval
function drawGraph(currentSensor, currentLocation, startDate, endDate) {
    $.ajax({
        url: 'api/1.0/data/list?sensor=' + currentSensor + '&location=' + currentLocation + '&start=' + startDate + '&end=' + endDate,
        success: function(data, status, ajax) {
            if (data.length === 0) {
                $('#demo').text("Sorry, no data delivered by server.");
                return;
            } else {
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
            }
        },
        error: function(ajax, status, error) {
            $('#demo').text("Sorry, can't load data.");
        },
        dataType: "json",
        headers: {
            accept: 'application/json'
        }
    });

}


//Signatur: sensorChanged: Number
//Descriptino: Action performed, if a sensor is selected
function sensorChanged(sensorId) {
    var currentLocation = getSelectedButtonValue('location');
    try {
        var i = slider.noUiSlider.get(); //Already a datums-slide in action?
        createDataview(sensorId, currentLocation, new Date(Number(i[0])).toISOString().substring(0, 19) + "Z", new Date(Number(i[1])).toISOString().substring(0, 19) + "Z");
    } catch (err) {
        createDataview(sensorId, currentLocation, 0, 0);
    }

}

//Signatur: locationChanged: Number
//Action performed if a location is selected
function locationChanged(locationId) {
    var currentSensor = getSelectedButtonValue('sensor');
    try {
        var i = slider.noUiSlider.get();
        createDataview(currentSensor, locationId, new Date(Number(i[0])).toISOString().substring(0, 19) + "Z", new Date(Number(i[1])).toISOString().substring(0, 19) + "Z");
    } catch (err) {
        createDataview(currentSensor, locationId, 0, 0);
    }
}


$(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $("input:radio[name=sensor]:first").attr('checked', true).trigger('change');
    $("input:radio[name=location]:first").attr('checked', true).trigger('change');
});


//Signatur: Number, Number, String, String
//Description: Wrapper to create the diagram and the Date-Slider
function createDataview(sensorId, locationId, start, end) {
    $.ajax({
        url: 'api/1.0/data/last?sensor=' + sensorId + '&location=' + locationId,
        success: function(data, status, ajax) {
            if (data.length < 1) {
                $('#demo').text("Sorry, can't load data.");
            } else {
                var dateOfLastMeasurement;
                var dayBevore;
                if (start === 0 || end === 0) { // Drawing the DateSlider for the fist time
                    dateOfLastMeasurement = new Date(data[0].datetime).toISOString().substring(0, 19) + "Z";
                    dayBevore = new Date(timestamp(data[0].datetime) - 17280000).toISOString().substring(0, 19) + "Z";
                    drawBar(dateOfLastMeasurement);
                } else { //Update the Dateslider
                    dateOfLastMeasurement = end;
                    dayBevore = start;
                }

                drawGraph(sensorId, locationId, dayBevore, dateOfLastMeasurement);
            }
        },
        error: function(ajax, status, error) {
            $('#demo').text("Sorry, can't load data.");
        },
        dataType: "json",
        headers: {
            accept: 'application/json'
        }
    });
}



// Create a new date from a string, return as a timestamp.
function timestamp(str) {
    return new Date(str).getTime();
}

// Create a string representation of the date.


// Needed to show currently set Date in Date-Slider
var
    weekdays = [
        "Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday",
        "Saturday"
    ],
    months = [
        "January", "February", "March",
        "April", "May", "June", "July",
        "August", "September", "October",
        "November", "December"
    ];

// Append a suffix to dates.
// Example: 23 => 23rd, 1 => 1st.
function nth(d) {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
        case 1:
            return "st";
        case 2:
            return "nd";
        case 3:
            return "rd";
        default:
            return "th";
    }
}


// Create a list of day and monthnames.

function formatDate(date) {
    return weekdays[date.getDay()] + ", " +
        date.getDate() + nth(date.getDate()) + " " +
        months[date.getMonth()] + " " +
        date.getFullYear();
}


//Signatur: drawBar: String
//Description: Draws a Date-Slider to a given max-Date (String). Min-Value is 2016-06-01
function drawBar(rangeMax) {
    var dateSlider = document.getElementById('slider');

    noUiSlider.create(dateSlider, {
        // Create two timestamps to define a range.
        range: {
            min: timestamp('2016-06-01'),
            max: timestamp(rangeMax)
        },

        // Steps of one week
        step: 1 * 24 * 60 * 60 * 1000,

        // Two more timestamps indicate the handle starting positions.
        start: [timestamp(rangeMax) - 172800000 * 2, timestamp(rangeMax)],
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
        var start = new Date(Number(values[0])).toISOString().substring(0, 19) + "Z";
        var end = new Date(Number(values[1])).toISOString().substring(0, 19) + "Z";

        var currentSensorId = getSelectedButtonValue('sensor');
        var currentLocationId = getSelectedButtonValue('location');
        drawGraph(currentSensorId, currentLocationId, start, end)
    });


}
