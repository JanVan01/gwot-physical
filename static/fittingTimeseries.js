// What are we doing here?
// So, we want two time series, adjust with respect to time, to each other.
// What I mean by that? Let's look at the picture:

//
// `+/:/+`        -+/://                         +/:/+.                                 `+/:/+`
//   +:   :s::::::::h    y/:::::::::::::::::::::::++   .h/////////////////////////////////s:   :+
//   `//://`        -//:/:                         //:/+`                                 `//://`
//
//
//
//    :/:/:    -/:/:.//:/.           `:/:/-    .:/:/.      -/:/:`            `:/:/-             -/:/:`
//   //   /o:::s`  .m.  `y:::::::::::s:   ++:::y`  `y:::::+o   -s::::::::::::y.   s:::::::::::::s`  .s
//   .+-.-+.```+:.-+o/--:+```````````-+-.-+.```//--:+`````.+-.-+-````````````:/-.:+`````````````+:.-/:
//     ...      `..` `..`             `...      `..`        ...`              `...               `..`
//

// Does it make sense to compare the i-th node of the first series with the i-th node of the second series.
// (Node correspondes to node-value).
// Probably not.

// What is a good races allocation?
// An assignment which minimizes the time distance between all measurements.
// But how do we get the best possible allocation regarding all the measurements?
//
// OPT (i, j) = max {OPT (i, j-1), OPT (i-1, j), 1/(| X [i] - Y [j] | ) + OPT (i-1, j-1) }
//


function TimeseriesMatching(X, Y, selector) {
    console.log("START TimeseriesMatching");

    console.log("X.length = " + X.length);
    console.log("Y.length = " + Y.length);
    var scalefactor = (new Date()).getTime() + 1000;
    console.log("scalefactor: " + scalefactor);


    var opt = [];
    for (var i = 0; i < X.length; i++) { // Number of rwos in Matrix
        var pushMe = [];
        for (var j = 0; j < Y.length; j++) { // Number or columns
            pushMe.push(null); // Initial value to check whether a value has been calculated
        }
        opt.push(pushMe);

    }



    innerMathing(X, Y, X.length - 1, Y.length - 1, selector, opt, scalefactor);



    // now reconstruct an alignment

    result = []; // Contains the input-Elements
    console.log("Reconstruct alignment from values");
    reconstruct(opt, X, Y, X.length - 1, Y.length - 1, result);

    return result;

}


function innerMathing(X, Y, x, y, selector, opt, scalefactor) {

    if (x < 0 || y < 0) {
        return 0;
    } else {
        var timeX = new Date(selector(X[x])).getTime();
        //console.log("timeX: " + timeX);

        var timeY = new Date(selector(Y[y])).getTime();
        //console.log("timeY: " + timeY);

        // Next we try to solve a minimization problem throw maxization by the means of DP / MM.
        // To do so we solve the problem with respect to the mutiplicative inverse of |timeX - timeY|
        // Our algebraic structure is a at least a body, so we can not devide by 0 which yield
        // to a problem if timeX == timeY.
        // We work around this porblem by defining values, wich are less then 10ms apart from each other as equivalent good. and return 1. The Value of this is the scalingfactor, which is due to its definition the largest value in our context.

        var timediv = Math.abs(timeX - timeY);
        // console.log("x = " + x + " und  y = " + y);
        // console.log("TimeDiv: " + timediv + " algoValue = " + scalefactor/timediv);
        if (timediv < 10) {
            timediv = 1;
        }

        if (!opt[x][y]) {
            opt[x][y] = Math.max(
                innerMathing(X, Y, x - 1, y, selector, opt, scalefactor),
                innerMathing(X, Y, x, y - 1, selector, opt, scalefactor),
                (scalefactor / timediv) + innerMathing(X, Y, x - 1, y - 1, selector, opt, scalefactor));
        }

        for (var i = 0; i < X.length; i++) {
            var row = [];
            for (var j = 0; j < Y.length; j++) {
                row.push(opt[i][j]);
            }
        }
        return opt[x][y];
    }

}

function reconstruct(opt, X, Y, x, y, output) {
    if (x === 0 || y === 0) {
        output.push({
            "x": X[x],
            "y": Y[y]
        });
        return;
    }

    if (opt[x - 1][y] === opt[x][y]) {
        reconstruct(opt, X, Y, x - 1, y, output);
    } else {
        if (opt[x][y - 1] === opt[x][y]) {
            reconstruct(opt, X, Y, x, y - 1, output);
        } else {
            output.push({
                "x": X[x],
                "y": Y[y]
            });
            reconstruct(opt, X, Y, x - 1, y - 1, output);
        }
    }


}
