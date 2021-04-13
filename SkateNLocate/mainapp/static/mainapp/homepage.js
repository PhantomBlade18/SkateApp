$('#nearMe').click(function () {
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
                    console.log(obj[0])
                    for (s in obj) {

                        var latlng = {
                            lat: obj[s].lat,
                            lng: obj[s].long
                        };

                        var add

                        console.log(obj[s].name)
                        text = '<div id="' + obj[s].id + '" class="skatepark">'
                        text += '<h3 id="location-name">' + obj[s].name + '</h3>'

                        add = geocoder.geocode({ location: latlng }, (results, status) => {
                            if (status === "OK") {
                                if (results[0]) {
                                    //alert(results[1].formatted_address)
                                    address = results[1].formatted_address
                                    alert(address)
                                    return address
                                } else {
                                    window.alert("No results found");
                                }
                            }
                            else {
                                window.alert("Geocoder failed due to: " + status);
                            }
                        });

                        text += '<h3 id="location-address">' + add + '</h3>'
                        text += '<input type="number" id="lat" hidden value=' + obj[s].lat + ' ><input type="number" id="lng" hidden value=' + obj[s].long + '>'
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