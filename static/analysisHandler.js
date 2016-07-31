var ac = new Actioncontroler();
ac.addAction('correlation', correlation);
// InitialValues
var startTime = new Date();
console.log("startTime setting = " + new Date(startTime));
var endTime = moment_fix(timerange.min).startOf('date').valueOf();
ac.updateSelectedTimeRange(startTime, endTime);

// Accessing ac from frontend
function analysisSelectionChanged(value) {
    ac.updateSelectedAction(value);
}

function sensorCompareChanged(id) {
    ac.updateSelectedSensorComprare(id);
}

function sensorChanged(id) {
    ac.updateSelectedSensor(id);
}

function locationChanged(id) {
    ac.updateSelectedLocation(id);
}

function outlierSelectionChanged(checked) {
    ac.updateOutlier(checked);
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
    var max_datetime = moment_fix(new Date()).endOf('date').valueOf();
    var min_datetime = moment_fix(timerange.min).startOf('date').valueOf();
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
        //var currentSensorId = getSelectedButtonValue('sensor');
        //var currentLocationId = getSelectedButtonValue('location');
        //drawGraph(currentSensorId, currentLocationId, values[0], values[1]);
        ac.updateSelectedTimeRange(values[0], values[1]);
    });



    // Signatur: getSelectedButtonValue: String -> int
    // Description: Returns the selected value of a set of radio buttons grouped by name.

}

function getSelectedButtonValue(name) {
    var selectedVal = 0;
    var selected = $("input[type='radio'][name='" + name + "']:checked");
    if (selected.length > 0) {
        selectedVal = selected.val();
    }
    return selectedVal;
}
