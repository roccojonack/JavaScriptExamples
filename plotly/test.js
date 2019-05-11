var trace1 = {
  x: [1, 2, 3, 4],
  y: [1, 4, 9, 16],
  name: 'Trace1',
  type: 'bar'
};
var trace2 = {
  x: [1, 2, 3, 4],
  y: [6, -8, -4.5, 8],
  name: 'Trace2',
  type: 'bar'
};
var trace3 = {
  x: [1, 2, 3, 4],
  y: [-15, -3, 4.5, -8],
  name: 'Trace3',
  type: 'bar'
 }

 var trace4 = {
  x: [1, 2, 3, 4],
  y: [-1, 3, -3, -4],
  name: 'Trace4',
  type: 'bar'
 }

var data = [trace1, trace2, trace3, trace4];
var layout = {
  xaxis: {title: 'X axis'},
  yaxis: {title: 'Y axis'},
  barmode: 'relative',
  title: 'Relative Barmode'
};

Plotly.newPlot('myDiv', data, layout);
