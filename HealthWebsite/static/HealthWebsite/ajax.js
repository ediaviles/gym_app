"use strict"

// == get posts
function GetGraphData() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr, true)
    }
    xhr.open("GET", json_data_url, true)
    xhr.send()
}


function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}


function updatePage(xhr, flag = true, lat = 0, lng = 0) {
    console.log("in updatePage")
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        if(flag){
            DisplayGraph(response)
        }
        else{
            DisplayMaps(response, lat, lng)
        }
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }
 
    console.log(xhr.responseText)
    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

// Needs a special function because there are multiple datasets for reps/squats
function CreateExerciseGraph(chart, data, labels, units, title) {
    const chartdata = {
        labels: labels,
        datasets: [
                {
                label: data[2][0],
                data: data[0],
                borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: Utils.transparentize(Utils.CHART_COLORS.red, 0.5),
                yAxisID: 'y',
                },
                {
                label: data[2][1],
                data: data[1],
                borderColor: 'rgb(54, 162, 235)',
                // backgroundColor: Utils.transparentize(Utils.CHART_COLORS.blue, 0.5),
                yAxisID: 'y1',
                }
                ]
            };
    var myChart = new Chart(chart, {
        type: 'line',
        data: chartdata,
        options: {
          responsive: true,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          stacked: false,
          plugins: {
            title: {
              display: true,
              text: title
            }
          },
          scales: {
            y: {
              type: 'linear',
              display: true,
              position: 'left',
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
      
              // grid line settings
              grid: {
                drawOnChartArea: false, // only want the grid lines for one axis to show up
              },
            },
          }
      }
});
}


function CreateGraph(chart, data, labels, type, title, units) {
    const opt = {
        responsiveness: true,
        scales: {
            y: {
                display: true,
                title: {
                    display: true,
                    text: units
                },
            },
        },
        plugins: {
            title: {
                display: true, 
                text: title
            }
        }
    }

    var myChart = new Chart(chart, {
        type: type,
        data: {
            labels: labels,
            datasets:[{
                label:'Daily Intake',
                data: data,
                backgroundColor: [ // FIXME: number of colors needs to be based on # of labels
                    'rgb(255, 99, 132)',
                    'rgb(252, 255, 35)',
                    'rgb(54, 162, 235)',
                    ],
                hoverOffset: 5
                }], 
            },
        options: opt
    });
} 



// = updateStream
function DisplayGraph(json) {
    // load in the chart options from the json
    let graphing = json["graphing"]
    let graph_data = json["data"]
    
    // This is so I know what page we are currently on
    document.getElementById("graphing").value = graphing
    
    
    for (let i = 0; i <= 3; i++) {
        // check for an existing chart and delete it
        // this is so we don't get an error when we make a new chart of the same name
        let id = 'chart' + i.toString();
        const existing_chart = Chart.getChart(id);
        if (existing_chart) {existing_chart.destroy()}
    }

    // the pos stays the same regardless of the selection, there are always 4
    let chart0 = document.getElementById('chart0').getContext('2d');
    let chart1 = document.getElementById('chart1').getContext('2d');
    let chart2 = document.getElementById('chart2').getContext('2d');
    let chart3 = document.getElementById('chart3').getContext('2d');
    if (graphing === "macros") {
        CreateGraph(chart0, graph_data["macros"][0]["breakfast"],   graph_data["macros"][1],    "doughnut", "Breakfast",    "grams") // breakfast
        CreateGraph(chart1, graph_data["macros"][0]["lunch"],       graph_data["macros"][1],    "doughnut", "Lunch",        "grams") // lunch
        CreateGraph(chart2, graph_data["macros"][0]["dinner"],      graph_data["macros"][1],    "doughnut", "Dinner",       "grams") // dinner
        CreateGraph(chart3, graph_data["macros"][0]["all"],         graph_data["macros"][1],    "doughnut", "All",          "grams") // all
    } else {
        CreateExerciseGraph(chart0, graph_data["squat"][0],     graph_data["squat"][1],     "line", "Squat",    "kg") // squat 
        CreateExerciseGraph(chart1, graph_data["bench"][0],     graph_data["bench"][1],     "line", "Bench",    "kg") // bench 
        CreateExerciseGraph(chart2, graph_data["deadlift"][0],  graph_data["deadlift"][1],  "line", "Deadlift", "kg") // deadlift 
        CreateGraph(        chart3, graph_data["weight"][0],    graph_data["weight"][1],    "bar",  "Weight",   "kg") // weight 
    }
}


function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

/* This function is ced by onclick on the functions selectiong what
 * I currently want to graph
 */
function GetSelect(obj) {
    // get the parameter the user wants to graph from the onclick function
    // and update the graph with this info
    let graphing = obj.id
    UpdateGraph(graphing)
}
function UpdateDates() {
    let graphing = document.getElementById("graphing").value
    console.log("updating the dates through the helper function")
    UpdateGraph(graphing)
}
// == addComment
function UpdateGraph(graphing) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    // Send the post request to the url which handles the JSON creation
    // If its getting a post request then it expects to get a see a graphing
    // parameter in the post req
    let startdate = document.getElementById("startdate").value
    let enddate = document.getElementById("enddate").value
    xhr.open("POST", json_data_url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(    "graphing="+graphing+
             "&"+"startdate="+startdate+
             "&"+"enddate="+enddate+
             "&"+"csrfmiddlewaretoken="+getCSRFToken());
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}


function initMap(){
    var myMapCenter = {lat: 40.785091, lng: -73.968285};

	// Create a map object and specify the DOM element for display.
	var map = new google.maps.Map(document.getElementById('map'), {
		center: myMapCenter,
		zoom: 14
	});

}

function GetGymData() {
    let xhr = new XMLHttpRequest()
    var loc = document.getElementById("address").value
    var geocoder = new google.maps.Geocoder();
    // var address = jQuery('#address').val();
    var latitude = 19.373341;
    var longitude = 78.662109;
    geocoder.geocode( { 'address': loc}, function(results, status) {
    
    if (status == google.maps.GeocoderStatus.OK) {
        latitude = results[0].geometry.location.lat();
        longitude = results[0].geometry.location.lng();
        } 
    }); 
    console.log(latitude, longitude)
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        console.log("in GetGymData")
        updatePage(xhr, false, latitude, longitude)
    }
    // var gym_data_url = "HealthWebsite/"
    var loc = new google.maps.LatLng(latitude, longitude)
    xhr.open("GET", "HealthWebsite/get-gyms/" + loc + "/", true)
    xhr.send()
}

function DisplayMaps(json,  lat = 0, lng = 0) {
    var mapOptions = {
        center:new google.maps.LatLng(lat, lng),
        zoom:7
     }
         
    var map = new google.maps.Map(document.getElementById("map"),mapOptions);
    for(let i = 0; i<json.length; i++){
        var marker = new google.maps.Marker({
            position: json[i][6],
            map: map,
            icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
              labelOrigin: new google.maps.Point(75, 32),
              size: new google.maps.Size(32,32),
              anchor: new google.maps.Point(16,32)
            }
        });
        marker.setMap(map)
    }
}
