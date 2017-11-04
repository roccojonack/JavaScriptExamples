
/* JAVASCRIPT CODE GOES HERE */
var table = $("#example").DataTable( );
var Title  = "account overview";
var xTitle = "date";
var yTitle = "amount";
var key_data_string;

function filterColumn ( i ) {
  $('#example').DataTable().column( i ).search(
					       $('#col'+i+'_filter').val(),
					       $('#col'+i+'_regex').prop('checked'),
					       $('#col'+i+'_smart').prop('checked')
					       ).draw();
}

function generateTable(data) {
  var dataSet = [];
  var startOfString = data.indexOf("\n",0);
  // console.log(data);
  do {
    var data1_string = data.substring(startOfString+1,data.indexOf("\n",startOfString+1));
    var data1_array  = data1_string.split(",");
    //console.log(data1_array);
    //console.log(startOfString);
    //console.log(data.length);
    dataSet.push(data1_array);
    startOfString = data.indexOf("\n",startOfString+1);
  } while (startOfString<(data.length-1))
    // console.log(dataSet);
    
    $.fn.dataTable.ext.search.push(
				   function( settings, data, dataIndex ) {
				     var min = $('#min').val();
				     var max = $('#max').val();
				     var age = data[0]; // use data for the age column
				     
				     // console.log("date parsing " + min + " " + max + " " + age);
				     if ( ( min.trim().length==0      && max.trim().length==0      ) ||
					  ( min.trim().length==0      && age.localeCompare(max)<=0 ) ||
					  ( min.localeCompare(age)<=0 && max.trim().length==0      ) ||
					  ( min.localeCompare(age)<=0 && age.localeCompare(max)<=0 ) )
				       {
					 return true;
				       }
				     return false;
				   }
				   );
  
  $.fn.dataTable.ext.search.push(
				 function( settings, data, dataIndex ) {
				   var min = parseFloat( $('#minAmount').val() );
				   var max = parseFloat( $('#maxAmount').val() );
				   var age = parseFloat( data[2] ) || 0; // use data for the age column
				   
				   // console.log("amount parsing " + min + " " + max + " " + age);
				   if ( ( isNaN( min ) && isNaN( max ) ) ||
					( isNaN( min ) && age <= max ) ||
					( min <= age   && isNaN( max ) ) ||
					( min <= age   && age <= max ) )
				     {
				       return true;
				     }
				   return false;
				 }
				 );
  
  table = $("#example").DataTable( {
    data: dataSet,
	"scrollX": true,
	columns: [
		  { title: "date" },
		  { title: "description" },
		  { title: "amount" },
		  { title: "category" },
		  { title: "account" }
		  ],
	columnDefs: [
		     { type: 'signed-num', targets: 2 }
		     ]
	} );
  
  $('input.column_filter').on( 
			      'keyup click', function () {
				filterColumn( $(this).parents('tr').attr('data-column') );
				// console.log(table.rows( { filter : 'applied' } ).data());
				myPlot(table.rows( { filter : 'applied' } ).data());
			      } );    
  
  // Event listener to the two range filtering inputs to redraw on input
  $('input.date_filter').on(
			    'keyup click', function() {
			      // console.log( table.rows( { filter : 'applied' } ).data() );
			      table.draw();
			      myPlot(table.rows( { filter : 'applied' } ).data());
			    } );
  $('input.amount_filter').on(
			      'keyup click', function() {
				// console.log(table.rows( { filter : 'applied' } ).data());
				table.draw();
				myPlot(table.rows( { filter : 'applied' } ).data());
			      } );
};
  
function convertStringToNumber(num){
  // console.log(num); 
  return parseFloat(num) || null;
}


// the main function is reading a CSV file, putting the data into a JS data structure
// and finally formats the data for plotly; setting up all layout information
// finally calling plotly itself
function myPlot(data) {
  //var my_data  = d3.csvParse(data);
  var my_data  = key_data_string + "\n";
  var index;
  for (index=0; index < data.length; index++) {
    // console.log(data[index]);  // raw CSV data
    my_data += data[index].toString();
    my_data += "\n";
  }
  console.log(data.length);  // length of vector
  // console.log(my_data);  // values to be ploted
  plotChart(my_data);
}

function plotChart(data) {
  var my_data  = d3.csvParse(data);
  // var my_data  = data;
  // console.log(my_data);  // raw CSV data
  // console.log(my_data.length);  // length of vector
  
  // first line contains the keys for different sets of values
  var key_data = key_data_string.split(",");
  //console.log(key_data);  // key labels
  
  // first row contains X axis values for all sets
  var xAxis = [];
  var index1;
  var index;
  for (index = 0; index < my_data.length; index++) {
    xAxis.push(my_data[index][key_data[0]]);
  };	
  // console.log(xAxis); 
  
  // all rows (except for first/second which is X) define Y values
  var yAxis       = [];
  var yAxis_tmp   = [];
  var start_index = 2;
  var end_index   = 4;
  var accumulate  = 0;
  var accumulateArray = [];
  index1    = 2;
  yAxis_tmp = [];
  for (index = 0; index < my_data.length; index++) {
    var amount = convertStringToNumber(my_data[index][key_data[index1]]);
    accumulate += amount;
    //console.log(amount);
    //console.log(accumulate);
    accumulateArray.push(accumulate);
    yAxis_tmp.push(amount);
  };
  yAxis.push(yAxis_tmp);
  yAxis.push(accumulateArray);
  index1 = 1;
  yAxis_tmp = [];
  for (index = 0; index < my_data.length; index++) {
    yAxis_tmp.push(my_data[index][key_data[index1]]);
  };
  yAxis.push(yAxis_tmp);
  
  //console.log(yAxis);
  // push data into data structure for plotly
  var trace1 = {
    x: xAxis,
    y: yAxis[0],
    name: 'amount',
    text: yAxis[2],
    //mode: 'lines+markers',
    //line: {shape: 'spline'},
    type: 'bar'
  };
  var trace2 = {
    x: xAxis,
    y: yAxis[1],
    name: 'sum',
    mode: 'lines+markers',
    line: {shape: 'hv'},
    //type: 'bar'
  };
  
  var data = [trace1,trace2];
  // setup layout information
  var layout = {
    title: Title,
    xaxis: {
      title: xTitle,
      type: 'date',
      tickfont: {
	size: 14,
	color: 'rgb(107, 107, 107)'
      },
    },
    yaxis: {
      title: yTitle,
      titlefont: {
	size: 16,
	color: 'rgb(107, 107, 107)'
      },
      tickfont: {
	size: 14,
	color: 'rgb(107, 107, 107)'
      }
    }
  };
  //console.log(trace);
  // actually call plotly
  Plotly.newPlot('chartCanvas', data, layout);
};

//add an event listener
d3.select("select").on(
	      "change", function(d) {
		var sel       = d3.select('#label-option').node().value + ".txt";
		// var xscale    = d3.select('#x-scale-option').node().value;
		console.log(sel);
		//console.log(xscale);
		// read actual CSV file; make sure no spaces!
		d3.text(sel, function(data) {
			  // setup the title based on comment if input file
			  console.log("Title is " + Title);
			  // setup the X axis title based on comment if input file
			  console.log("xTitle is " + xTitle);
			  // setup the Y axis title based on comment if input file
			  console.log("yTitle is " + yTitle);
			  // remove all comments before passing into data structure
			  data = data.replace(/^[#@][^\r\n]+[\r\n]+/mg, ''); 
			  // console.log("data is " + data);
			  // var my_data  = d3.csvParse(data);
			  key_data_string = data.substring(0,data.indexOf("\n"));
			  
			  plotChart(data);
			  table.destroy();
			  generateTable(data);
			} 
			);
	      } 
);
