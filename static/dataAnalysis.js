function COR(X, Y, selector) { // deviation from namingconventions for functions due to conventions for statistic functions
    if (!X || !Y) {
        $('#demo').text("Sorry, there is no data available for your selected criteria. Extend the time-range or choose other sensors/location.");
    }
    if (typeof selector === 'undefined') {
        selector = function(x) {
            return x;
        };
    } else {
        var meanX = getMean(X, selector);
        var meanY = getMean(Y, selector);
        console.log(meanX);
        console.log(meanY);
        var result = 0;
        var xs = 0;
        var ys = 0;

        for (var i = 0; i < X.length; i++) {
            result = result + (selector(X[i]) - meanX) * (selector(Y[i]) - meanY);
        }
        for (var j = 0; j < X.length; j++) {
            xs = xs + Math.pow((selector(X[j]) - meanX), 2);
        }

        for (var l = 0; l < Y.length; l++) {
            ys = ys + Math.pow((selector(Y[l]) - meanY), 2);
        }
        return result / (Math.sqrt(xs * ys));
    }

}

function getMean(x, selector) {
    if (typeof selector === 'undefined') {
        selector = function(x) {
            return x;
        }
    }
    if (x) {
        var sum = 0;
        for (var i = 0; i < x.length; i++) {
            sum = sum + selector(x[i]);
        }
        return sum / x.length;
    } else {
        return null;
    }
}
