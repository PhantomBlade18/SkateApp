$('#nearMe').click(function () {
    if (navigator.geolocation) {
        let options = {
            enableHighAccuracy: true,
        } 
        navigator.geolocation.getCurrentPosition((position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos)
            $.ajax({
                method: 'POST',
                url: 'Nearby/',
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                data: {
                    lat: pos.lat,
                    lng: pos.lng,
                },
                success: function (data) {
                    console.log(data)
                    var obj = JSON.parse(data["skateparks"])
                    var log = data["loggedin"]



                    $('#skateparks-list').empty()
                    //console.log(obj[0])
                    for (s in obj) {

                        var latlng = {
                            lat: obj[s].lat,
                            lng: obj[s].long
                        };
                        var attributes = "";
                        if (obj[s].ramps == 1) {
                            attributes += "<li>Ramps</li>  "
                        }
                        if (obj[s].indoor == 1) {
                            attributes += "<li>Indoors</li>  "
                        }
                        if (obj[s].paid == 1) {
                            attributes += "<li>Paid</li>  "
                        }
                        else {
                            attributes += "<li>Free</li>  "
                        }
                        if (obj[s].crusing == 1) {
                            attributes += "<li>Cruising</li>  "
                        }
                        else {
                            attributes += "<li>Tricks</li>  "
                        }
                        if (obj[s].asphalt == 1) {
                            attributes += "<li>Asphalt</li>  "
                        }
                        if (obj[s].concrete == 1) {
                            attributes += "<li>Concrete</li>  "
                        }
                        if (obj[s].wood == 1) {
                            attributes += "<li>Wood</li>  "
                        }
                        if (obj[s].skateType == 1) {
                            attributes += "<li>Skateboard</li>  "
                        }
                        else if (obj[s].skateType == 2) {
                            attributes += "<li>Any</li>  "
                        }
                        else if (obj[s].skateType == 3) {
                            attributes += "<li>Longboard</li> "
                        }

                        //console.log(obj[s].name)
                        text = '<div id="' + obj[s].id + '" class="skatepark">'
                        text += '<h3 id="location-name">' + obj[s].name + '</h3>'

                        text += '<input type="number" id="lat" hidden value=' + obj[s].lat + ' ><input type="number" id="lng" hidden value=' + obj[s].long + '>'
                        text += '<div class="row">'
                        text += '<div class="col-3" id = "popularityScore"><p>Popularity: ' + obj[s].avgPopularity.toFixed(2) + '</p></div >'
                        text += '<div class="col-3" id = "avgScore"><p >Average: ' + obj[s].avgRating.toFixed(2) + '</p></div >'
                        text += '<div class="col-3" id = "SurfaceScore"><p >Surface: ' + obj[s].avgSurface.toFixed(2) + '</p></div >'
                        text += '</div >'
                        text += '<ul id = "attributes"> <b>Properties </b>'+ attributes + '</ul>'
                        text += '<p id = "distance">Distance : ' + obj[s].distance.toFixed(2) + ' km</p>'
                        text += '<a class="showMe btn btn-primary" href="#map"> Show me </a> \n'
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
                        var contentString = "<p>" + obj[s].name + " <p>"
                        const infowindow = new google.maps.InfoWindow({
                            content: contentString,
                        });
                        var marker = new google.maps.Marker({
                            position: latlng,
                            map: map,
                            title: obj[s].name,
                        });
                        marker.addListener("click", () => {
                            infowindow.open(map,marker);
                        });


                    }
                    $('.rate-form').hide();
                }
            })
        },anError(),options)
    }
    else {
        alert("Browser does not support Location Tracking");
    }
})


function anError() {
    console.log("An error has occurred")
}