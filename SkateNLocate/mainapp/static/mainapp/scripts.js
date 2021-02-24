$(document).ready(initMap)

var lat = 0
var lng = 0
var map
var geocoder 

function initMap() {
    // The location of Uluru
    pos = { lat: 25, lng: 36 }

    const uluru = { lat: -24.344, lng: 132.036 };
    // The map, centered at Uluru
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: pos,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
        position: pos,
        map: map,
    });

    geocoder = new google.maps.Geocoder();
}

function getPosition() {
    pos = { lat: 51.548600, lng: -0.367310 };
    f = new google.maps.LatLng(pos.lat,pos.lng)
    map.setCenter(f);
}

$('#testButton').click(getPosition);
$('#search').click(getAddress)

function getAddress() {
    address = $('#address').val()
    geocoder.geocode({ address: address }, (results, status) => {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        }
        else {
            alert("Geocode was not succeessful. Reason: " + status);
        }
    });
}