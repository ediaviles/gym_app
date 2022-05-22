"use strict"
var temp;
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

function loadAddresses(){
    let xhr = new XMLHttpRequest()
    console.log("address_url",address_data_url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updateAddresses(xhr)
    }
    //FindBuddies();
    var address = document.getElementById('address').value;
    xhr.open("POST", address_data_url, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("address="+address+"&csrfmiddlewaretoken="+getCSRFToken());
    //var modal = document.getElementById("exampleModalCenter");

}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateAddresses(xhr){
    if (xhr.status == 200) {
        // console.log("xhr.responseText",xhr.responseText);
        let response = JSON.parse(JSON.stringify(xhr.responseText));
        if(response) {
            console.log("response", response);
            AddressList(response)
            return
        }
    
        if (response.hasOwnProperty('error')) {
            displayError(response.error)
            return
        }
    }
    
    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }
    
    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }
    
    let response = JSON.parse(JSON.stringify(xhr.responseText));
    displayError(response)
}

function AddressList(response){
    console.log("WE HERE");
    let list = document.getElementById("user-address")
}

function FindBuddies(){
    var address = document.getElementById('address').value;
    var pos = GetCoor(address);
    // callback(pos);
    // console.log("lol", pos);
    // var buddies = GetBuddies(pos);
}

async function GetBuddies(pos1) {
    //let dest = "1055 Morewood Place, Pittsburgh, PA"
    //var pos2 = await GetCoor(dest);
    var pos2 = {lat: 40.446010, lng: -79.942030};
    // callback(pos2);
    // console.log("pos1:", pos1);
    // console.log("pos2:", pos2);
    var maxDistance = null;
    for(let i = 0; i < 1; i++) {
        // map.setCenter(pos);
        // console.log("Buddies", pos1, pos2);
        var distance = initBuddy(pos1, pos2);
        // callback(distance);
        // console.log("returned");
        // new google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(pos1),new google.maps.LatLng(pos2));
        // console.log("distance", distance);
        if(maxDistance == null || distance > maxDistance){
            maxDistance = distance;
        }
    }
}

function GetCoor(address) {
    // console.log(address)
    var geocoder= new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
        // console.log(results);
        var lat = results[0].geometry.location.lat();
        var lng = results[0].geometry.location.lng();
        var pos = {lat:parseFloat(lat), lng:parseFloat(lng)};
        // console.log("1.", pos)
        // _callback();
        temp = pos;
        
        // console.log("temp",results);

        GetBuddies(pos);
    } else {
        var pos = {lat: 40.437450, lng: -79.990585};
        temp = pos;
    }
    });

}

function initBuddy(point1, point2){
    let directionsService = new google.maps.DirectionsService();
    let directionsRenderer = new google.maps.DirectionsRenderer();
    // directionsRenderer.setMap(map); // Existing map object displays directions
    // Create route from existing points used for markers
    // console.log(point1, point2);
    const route = {
        origin: point1,
        destination: point2,
        travelMode: 'DRIVING'
    } 

    directionsService.route(route,
    // capture directions
    function(response, status) {
        // console.log(status);
        if (status !== 'OK') {
            window.alert('Directions request failed due to ' + status);
            // _callback();
            return;
        } else {
            directionsRenderer.setDirections(response); // Add route to the map
            var directionsData = response.routes[0].legs[0]; // Get data about the mapped route
            console.log("initBuddy",directionsData);
            if (!directionsData) {
                window.alert('Directions request failed');
                // _callback();
                return;
            } else {
                document.getElementById('msg').innerHTML = " Travel distance is " + directionsData.distance.text + " (" + directionsData.duration.text + ").";
            }
        }
    });
    // _callback();
}

function AddFriend(flag) {
    if(flag){

    }
}