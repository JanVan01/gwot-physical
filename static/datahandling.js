var uncertainty = function(value, quality){
 var result = [];
 var start = null;
 for(var i=1; i < value.length; i++){ // i = 1, da i=0 die Datenbeschreibung enthält
 if(!start && quality[i] == 0){
   start = value[i];
 }
 if(!!start && quality[i] == 1){
   result.push({
     start: start,
     end: value[i]
   })
start = null;
 }
 }
return result;
}

var maxim = function(values, quality){
  var maxi = ["maximum"];
  var i = 1;
  //Find first measurement of quality 1 to use it as base-value
  for(var k = i; k < values.length; k++){
    if(quality[k] != 1){
      maxi.push(null);
    }
    else{
      maxi.push(values[k]);
      i = k+1;
      k = values.length;
    }
  }


    for(var k = i; k < values.length; k++){
      if(quality[k] == 1 && values[k] > maxi[k-1]){
        maxi.push(values[k]);
      }
      else{
        maxi.push(maxi[k-1]);
      }
}
return maxi;
}

var min = function(values, quality){
  var min = ["minimum"];
  var i = 1;
  //Find first measurement of quality 1 to use it as base-value
  for(var k = i; k < values.length; k++){
    if(quality[k] != 1){
      min.push(null);
    }
    else{
      min.push(values[k]);
      i = k+1;
      k = values.length;
    }
  }


    for(var k = i; k < values.length; k++){
      if(quality[k] == 1 && values[k] < min[k-1]){
        min.push(values[k]);
      }
      else{
        min.push(min[k-1]);
      }
}
return min;
}
