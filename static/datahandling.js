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


// Signatur: makeRadioButton(String, Object, String) -> label
// Description: Takes name(String), value(Object) and text(String) for a radio button and returns a radiobutton(label)
function makeRadioButton(name, value, text) {

    var label = document.createElement("label");

    var radio = document.createElement("input");
    label.setAttribute("data-toggle", "tooltip");
    label.setAttribute("data-placement", "top");
    label.setAttribute("title", text);
    radio.type = "radio";
    radio.name = name;
    radio.value = value;
    label.appendChild(radio);
    label.appendChild(document.createTextNode(text));
    return label;
}

// Signatur: selectButtonsByName: String -> Array
// Description: Takes a name (String) and returns all input-Elements with this name. In this context: RadioButtons
function selectButtonsByName(name) {
    var allSensors = document.getElementsByTagName("input");
    var result = [];

    for (var i = 0; i < allSensors.length; i++) {
        if (allSensors[i].name === name) {
            result.push(allSensors[i]);
        }
    }
    return result;
}


// Signatur: getSelectedButton: Array -> input-Element
// Description: Takes an array of Buttons and returns the checked Button.
function getSelectedButton(sensors) {
    var result = [];
    for (var i = 0; i < sensors.length; i++) {
        if (sensors[i].checked) {
            result.push(sensors[i]);
            i = sensors.length; // Only one button is checked at the time in each group
        }
    }

    return result;
}

// Signatur: getValuesBySensorId: Array, Array, Number -> Object
// Description: Returns an Array of measurements which are associated with a given sensorId
function getValuesBySensorId(measurements, measurementSensorIds, sensorId) {
    var result = [];
    for (var i = 0; i < measurementSensorIds.length; i++) {
        if (measurementSensorIds[i] == sensorId) {
            result.push(measurements[i]);
        }
    }
    return result;
}

// Signatur: getMeasurements: Array, Array, Number, Array, Array, Number, Array -> dictionary
// Description: Returns to given locationId and SensorID the measurements at the location for the sensor with quality and time
function getMeasurements(time, measurementQualities, selectedLocationId, locationIdOfMeasurement, measurementSensorIds, currentSensor, measurements){
  var selectetMeasurements = ['measurements'];
  var selectedTime = ['time'];
  var quality = [];
  for(var i = 0; i < measurements.length; i++){
    if(Number(currentSensor) == measurementSensorIds[i] && Number(selectedLocationId) == Number(locationIdOfMeasurement[i])){
        selectetMeasurements.push(measurements[i]);
        selectedTime.push(time[i]);
        quality.push(measurementQualities[i]);
    }
  }
  return {'values': selectetMeasurements, 'time': selectedTime, 'quality': quality};
}


//Signatur: getMeasurementUnits: Array, Array, Number -> String
//Description: Returns to a given id of a sensor its unit of measurements
function getMeasurementUnits(sensorUnits, sensorIds, currentSensorID) {
  var result = '';
  for(var i = 0; i < sensorIds.length; i++){
    if(currentSensorID == sensorIds[i]){
      result = result + sensorUnits[i];
    }
  }

  return result;
}


//Signatur: getButtonById: Array, Number -> input-Element
//Description: Takes an Array of input-Elements (buttons) and an id. Returns the button with the corresponding id, else null.
function getButtonById(buttons, id) {
    for (var i = 0; i < buttons.length; i++) {
        if (Number(buttons[i].value) == id) {
            return buttons[i];

        }
    }
    return null;
}


//Signatur: setFirstLocationAndSensorWithValues; Array, Array
//Description: Takes the location-ids and ids of measuring sensors. onclicks the first location and sensor -combination which offer data.
// If no combination with data exists, this is shown in div with id "demo" and all radiobuttons are disabled
function setFirstLocationAndSensorWithValues(locationIdOfMeasurement, measurementSensorIds) {

    if (locationIdOfMeasurement.length > 0) {
        // Returning the last id-Pair of location and Sensor, which measured. Otherwise after a first measurement, the old location will always show up first
        // That would be not good.
        var locationID = locationIdOfMeasurement[locationIdOfMeasurement.length - 1];
        var sensorID = measurementSensorIds[measurementSensorIds.length - 1];
        var sensorButtons = selectButtonsByName('sensor');
        var locationButtons = selectButtonsByName('location');

        var sensor = getButtonById(sensorButtons, sensorID);
        var location = getButtonById(locationButtons, locationID);

        sensor.click();
        location.click();
    } else {
        document.getElementById("demo").innerHTML = "No data!";
        var allSensors = document.getElementsByTagName("input");
        var allSensors = document.getElementsByTagName("input");

        for (var i = 0; i < allSensors.length; i++) {
            allSensors[i].disabled = true;
        }

    }

}


//Signatur: disableButtons: Array
//Description: disables all buttons in an Array
function disableButtons(buttons){
  for(var i = 0; i < buttons.length; i++){
    buttens[i].disabled = true;
  }
}

//Signatur: enableButtons: Array
//Description: enables all buttons
function enableButtons(buttons){
  for(var i = 0; i < buttons.length; i++){
    buttens[i].disabled = false;
  }
}


//Signatur: enableOnlySensorsWithMeasurements: Number, Array, Array, String -> input-Element
//Description: Enables only Sensor-Buttons which can be associated to measurements, any orher Sensor-Button is disabled.
// Because the current selected button my be disabled, the finction returns a new selected button which is associated to measurement-values.

function enableOnlySensorsWithMeasurements(selectedLocationId, locationIdOfMeasurement, measurementSensorIds,type){
  var sensorIdsAtLocation = new Set();
  for(var i = 0; i < locationIdOfMeasurement.length; i++){
    if(selectedLocationId == locationIdOfMeasurement[i]){
      sensorIdsAtLocation.add(Number(measurementSensorIds[i]));
    }
  }

  var allSensorButtons = selectButtonsByName(type);
  var clicked = false;
  var newCurrentSensor;
  for(var i = 0; i < allSensorButtons.length; i++){
    if(sensorIdsAtLocation.has(Number(allSensorButtons[i].value))){
      allSensorButtons[i].disabled = false;
      if(!clicked){
        allSensorButtons[i].click();
        clicked = true;
        newCurrentSensor = allSensorButtons[i].value;
      }
    }
    else{
      allSensorButtons[i].disabled = true;
    }
  }
  return newCurrentSensor;
}



function drawGraph (sensorIds, sensorUnits, currentSensor, currentLocation) {
  $.ajax({
      url: 'api/1.0/data/list?sensor=' + currentSensor + '&location=' + currentLocation,
      success: function(data, status, ajax) {
          var dateTime = ['time'];
          var measurements = ['measurements'];
          var measurementQuality = [];
          for (i = 0; i < data.length; i++) {
              dateTime.push(data[i].datetime);
              measurements.push(data[i].value);
              measurementQuality.push(data[i].quality);
          }
          if(measurements.length < 2){
            measurements.push(0);
            dateTime.push("1900-01-01T00:00:11.080805");
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
                  //extent: [dateTime[dateTime.length - 2], dateTime[dateTime.length - 1]],
                  x: {
                      type: 'timeseries',
                      tick: {
                          format: '%Y-%m-%d %H-%M',
                          count: 1 + Math.ceil(dateTime.length / (dateTime.length / 4))
                      }
                  },
                  y: {
                      label: String(getMeasurementUnits(sensorUnits, sensorIds, currentSensor))
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
      error: function(ajax, status, error) {
          alert("Sorry, can't load data.");
      },
      dataType: "json",
      headers: {
          accept: 'application/json'
      }
  });
}



$(function() {
        $('[data-toggle="tooltip"]').tooltip()
    });
