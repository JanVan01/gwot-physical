var Actioncontroler = function(datacontroler) {
    var actions = {}; // stores actions as key-value pairs
    var selectedAction= 'correlation';
    var selectedSensor = Number(getSelectedButtonValue("sensor"));
    var selectedSensorCompare = Number(getSelectedButtonValue("sensorCompare"));
    var selectedLocation = Number(getSelectedButtonValue("location"));;
    var selectedTimeRange = [];
    var excludeOutliers = true;



    // Takes a name for an action and an action and adds that as key-value pair to actions
    this.addAction = function(name, action) {
        actions[name] = action;
        console.log("actions are: " + actions);
    }

    this.updateOutlier = function (checked) {
      excludeOutliers = checked;
      console.log("excludeOutliers: " + excludeOutliers);
      this.runAction();
    }

    this.updateSelectedLocation = function (id) {
      selectedLocation = id;
      console.log("selectedLocation is: " + selectedLocation);
      this.runAction();
    }

    // Fetches all selected radiobutons.
    this.updateSelectedSensor = function(id) {
        selectedSensor = id;
        console.log("selectedSensor is: " + selectedSensor);
        this.runAction();
    }

    // Fetches all selected radiobutons.
    this.updateSelectedSensorComprare = function(id) {
        selectedSensorCompare = id;
        console.log("selectedSensorCompare is: " + selectedSensorCompare);
        this.runAction();
    }


    // Push-style Method (friend-method for the time-slider) to push changed time-Range
    this.updateSelectedTimeRange = function(start, end) {
        selectedTimeRange = [start, end]
        console.log("Timerange is: " + selectedTimeRange);
        this.runAction();
    }

    // Updates the selected Action - Push-style
    this.updateSelectedAction = function(actionName) {
        selectedAction = actionName;
        this.runAction();
    }


    this.runAction = function() {
      $('#demo').text("Processing");
      console.log("run Action");
        actions[selectedAction]([selectedSensor, selectedSensorCompare], selectedLocation, selectedTimeRange[0], selectedTimeRange[1], excludeOutliers);
    }

}
