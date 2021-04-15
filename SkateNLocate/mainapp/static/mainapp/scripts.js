$(document).ready(initMap)

var lat = 0
var lng = 0
var map
var geocoder
var ran

function initMap() {
    // The location
    pos = { lat: 25, lng: 36 }
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: pos,
    });
    // The marker, positioned at Uluru

    geocoder = new google.maps.Geocoder();
    $('#nearMe').trigger('click');
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
            ran = results[0].formatted_address;
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
                    var obj = JSON.parse(data["skateparks"])
                    var log = data["loggedin"]

                    

                    $('#skateparks-list').empty()
                    //console.log(obj[0])
                    for (s in obj) {

                        var latlng = {
                            lat: obj[s].lat,
                            lng: obj[s].long
                        };

                        var add

                        //console.log(obj[s].name)
                        text = '<div id="' + obj[s].id + '" class="skatepark">'
                        text += '<h3 id="location-name">' + obj[s].name + '</h3>'

                        text += '<input type="number" id="lat" hidden value=' + obj[s].lat + ' ><input type="number" id="lng" hidden value=' + obj[s].long +'>'
                        text += '<p id = "popularityScore">Popularity: ' + obj[s].avgPopularity + '</p>'
                        text += '<p id = "avgScore">Average: ' + obj[s].avgRating + '</p>'
                        text += '<p id = "SurfaceScore">Surface: ' + obj[s].avgSurface + '</p>'
                        text += '<p id = "distance">Distance : ' + obj[s].distance.toFixed(2) + ' km</p>'
                        text += '<button class="showMe btn btn-primary"> Show me </button> \n'
                        if (log == true) {
                            text += '<button class="rateMe btn btn-primary"> Rate </button>'
                            text += '<div class="rate-Form">'
                            text += '<label for="overall">Overall Score:</label>'
                            text += '<select id="overall" name="overall" class="custom-select">'
                            text += '<option value="5">5-Great</option>'
                            text += '<option value="4">4-Good</option>'
                            text += '<option value="3">3-Average</option>'
                            text += '<option value="2">2-Bad</option>'
                            text += '<option value="1">1-Horrible</option>'
                            text += '</select>'
                            text += '<label for="popularity">Crowd Level:</label>'
                            text += '<select id="popularity" name="popularity" class="custom-select">'
                            text += '<option value="5">5-Quiet</option>'
                            text += '<option value="4">4-A few Skaters</option>'
                            text += '<option value="3">3-Moderate</option>'
                            text += '<option value="2">2-Busy</option>'
                            text += '<option value="1">1-Very Crowded</option>'
                            text += '</select>'
                            text += '<label for="surface">Surface Quality:</label>'
                            text += '<select id="surface" name="surface" class="custom-select">'
                            text += '<option value="5">5-Great</option>'
                            text += '<option value="4">4-Good</option>'
                            text += '<option value="3">3-Average</option>'
                            text += '<option value="2">2-Bad</option>'
                            text += '<option value="1">1-Horrible</option>'
                            text += '</select>'
                            text += '\n<button class="submitRating btn btn-primary">Submit Rating </button></div>'
                        }
                        
                        text += '</div>'
                        $('#skateparks-list').append(text)
                        var contentString = "<p>"+ obj[s].name+" <p>"
                        const infowindow = new google.maps.InfoWindow({
                            content: contentString,
                        });
                        var marker = new google.maps.Marker({
                            position: latlng,
                            map: map,
                            title: obj[s].name,
                        });
                        marker.addListener("click", () => {
                            infowindow.open(map, marker);
                        });
                        
                    }
                    $('.rate-form').hide();
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

$('#skateparks-list').on('click','.showMe',function () {
    var id = $(this).parent().attr("id")
    //$(this).sibling("lat").val
    //$(this).sibling("lng").val
    var latlng;
    latlng = { lat: parseFloat($(this).siblings("#lat").val()), lng: parseFloat($(this).siblings("#lng").val()) }
    map.setCenter(latlng)
    geocoder.geocode({ location: latlng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                //alert(results[1].formatted_address)
                address = results[1].formatted_address
                $('#focused-park').empty();
                $('html').animate({ scrollTop: $('#focused-park').offset().top }, 2000);
                var text = "";
                text += '<h3>' + $(this).siblings("#location-name").text() + '</h3>';
                text += '<p id = "address">Address: ' + address + '</p>';
                text += '<p id = "popularityScore">Popularity: ' + $(this).siblings('#popularityScore').text() + '</p>';
                text += '<p id = "avgScore">Average: ' + $(this).siblings('#avgScore').text() + '</p>';
                text += '<p id = "SurfaceScore">Surface: ' + $(this).siblings('#SurfaceScore').text() + '</p>';
                text += '<p id = "distance">Distance : ' + $(this).siblings('#distance').text() + '</p>';
                $('#focused-park').append(text);

            } else {
                window.alert("No results found");
            }
        }
        else {
            window.alert("Geocoder failed due to: " + status);
        }
    });
    map.setZoom(14)

})

$('#skateparks-list').on('click', '.rateMe', function () {
    $(this).siblings(".rate-Form").show();
})


$('#skateparks-list').on('click', '.submitRating', function () {
    var id = $(this).parent().parent().attr('id')
    var avg = $(this).siblings('#overall').val()
    var sur = $(this).siblings('#surface').val()
    var pop = $(this).siblings('#popularity').val()
    var form = $(this)
    $.ajax({
        method: "POST",
        url: 'submitRating/',
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        data: {
            id: id,
            avg: avg,
            sur: sur,
            pop: pop,

        },
        success: function (data) {
            if (data['successful'] == true) {
                alert(data['msg'])
                form.parent().hide()
                //$(this).parent().hide()
            }
            else {
                alert("Rating unsuccessful")
            }
        }
    })

})
