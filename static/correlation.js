function correlation(currentSensors, currentLocation, startDate, endDate, outliers) {

    var url = 'api/1.0/data/list?limit=10000&sensor=' + currentSensors.toString() + '&location=' + currentLocation;
    if (startDate) {
        startDate = moment_fix(parseInt(startDate)).startOf('date').format();
        url += '&start=' + startDate;
    }
    if (endDate) {
        endDate = moment_fix(parseInt(endDate)).endOf('date').format();
        url += '&end=' + endDate;
    }
    if (outliers) {
        url += '&quality=0.5';
    }
    $.ajax({
        url: url,
        success: function(data, status, ajax) {

          if (currentSensors[0] == currentSensors[1]) {
              plotTimeseries(1, data, data, function(t) {
                  return t.datetime
              }, function(v) {
                  return v.value;
              });
              return;
          }

            if (data.length < 12) { // at leat 6 measurements for each sensor, setting this as minimum for calculating a correlation
                $('#demo').text("Sorry, there is no data available for your selected criteria. Extend the time-range or choose other sensors/location.");
                return;
            } else {

                var X = []; // Upper-Case letter due to the context of timeseriesanalysis
                var Y = [];

                ;
                // grouping elementy by id
                for (element of data) {
                    if (element.sensor.id == currentSensors[0]) {
                        X.push(element);
                    } else {
                        Y.push(element);
                    }
                }


                if (X.length < 6 || Y.length < 6) { // at leat 6 measurements for each sensor, setting this as minimum for calculating a correlation
                    $('#demo').text("Sorry, there is no enough data available for the calculations. Extend the time-range or choose other sensors/location.");
                    return;
                }

               

                // now deciding wich elements are to be paired for calculating the correlation
                // for more information: see corresponding file

                var cp = TimeseriesMatching(X, Y, function(x) {
                    return x.datetime;
                });

                // if what we get back from cp sufficient to calculate a correlation?
                //
                if (cp.length < 6) {
                    $('#demo').text("Sorry, there is no data available for your selected criteria. Extend the time-range or choose other sensors/location.");
                    return;
                }


                // Lets calculate the R-Value:

                // Group objects
                var Xnew = [];
                var Ynew = [];
                for (var i = cp.length - 1; i > 0; i--) {
                    Xnew.push(cp[i]['x']);
                    Ynew.push(cp[i]['y']);
                }

                for (var element of Ynew) {}

                var rval = COR(Xnew, Ynew, function(x) {
                    return x.value;
                });
                plotTimeseries(rval, Xnew, Ynew, function(t) {
                    return t.datetime
                }, function(v) {
                    return v.value;
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
