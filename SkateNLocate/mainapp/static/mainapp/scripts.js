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
        zoom: 14,
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

$('#search').click(findAddress)

//searches for position, zooms to it and places down a marker
function findAddress() {
    address = $('#address').val()
    geocoder.geocode({ address: address, region: "uk" }, (results, status) => {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            console.log(results)
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

//function translates stored lat long coordinates into an address to help the user find park
function geoCodeAddress(latlng) {
    geocoder.geocode({ location: latlng}, (results, status) => {
        if (status === 'OK') {
            console.log(results[0])
            return results[0].formatted_address;
        }
        else {
            console.log("Geocode was not succeessful. Reason: " + status);
        }
    });
}


//homes in on users rough location based on coordinates provided
$('#nearMe').click(function(){
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos)
            $.ajax({
                method: 'POST',
                url: 'recommendations/',
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                data: {
                    lat: pos.lat,
                    lng: pos.lng,
                },
                success: function (data) {
                    var obj = JSON.parse(data)
                    console.log("boop");
                    console.log(obj[0])
                    for (s in obj) {
                        console.log(obj[s].name)
                        text = '<div id="' + obj[s].id + '" class="skatepark">'
                        text += '<h3>' + obj[s].name + '</h3>'
                        latlng = { lat: parseFloat(obj[s].lat), lng: parseFloat(obj[s].long) }
                        add = geoCodeAddress(latlng)
                        text += '<p id= "address-line">' + +'</p>'
                        text += '</div>'
                        $('#skateparks-list').append(text)

                    }
                }
            })
        })
    }
    else {
        alert("Browser does not support Location Tracking");
    }
})



//auto triggers specific button
function test() {
    $('#search').trigger('click');
}

