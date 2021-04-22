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
            //console.log(results)
        
        }
        else {
            alert("Geocode was not succeessful. Reason: " + status);
        }
    });
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
                var text = "";
                text += '<h3>' + $(this).siblings("#location-name").text() + '</h3>';
                text += '<p id = "address">Address: ' + address + '</p>';
                text += '<p id = "popularityScore">' + $(this).siblings('.row').children('#popularityScore').text() + '</p>';
                text += '<p id = "avgScore">Average: ' + $(this).siblings('.row').children('#avgScore').text() + '</p>';
                text += '<p id = "SurfaceScore">Surface: ' + $(this).siblings('.row').children('#SurfaceScore').text() + '</p>';
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

$('#ChangeEmail').click(function (e) {
    e.preventDefault();
    var nemail = $('input[name=email]').val()
    $.ajax({
        method: "POST",
        url: 'updateEmail/',
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        data: {
            email: nemail,
        },
        success: function (data) {
            if (data['successful'] == true) {
                alert(data['msg'])
                //$(this).parent().hide()
            }
            else {
                alert("Your email could not be updated at this time. Please try again later.")
            }
        }
    })
})

$('#ChangePassword').click(function (e) {
    e.preventDefault();
    var cPass = $('input[name=currentPassword]').val()
    var nPass = $('input[name=newPassword]').val()
    $.ajax({
        method: "POST",
        url: 'updatePassword/',
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        data: {
            currentPassword: cPass,
            newPassword: nPass
        },
        success: function (data) {
            if (data['successful'] == true) {
                alert(data['msg'])
                //$(this).parent().hide()
            }
            else {
                alert("Your email could not be updated at this time. Please try again later.")
            }
        }
    })
})

$('#updatePreferences').click(function (e) {
    e.preventDefault();
    $.ajax({
        method: "POST",
        url: 'updatePreferences/',
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        data: {
            ramps: $('input[name=ramps]:checked').val(),
            indoor: $('input[name=indoors]:checked').val(),
            paid: $('input[name=paid]:checked').val(),
            cruising: $('input[name=cruising]:checked').val(),
            asphalt: $('input[name=asphalt]:checked').val(),
            concrete: $('input[name=concrete]:checked').val(),
            wood: $('input[name=wood]:checked').val(),
            board: $('select[name=board]').val(),
        },
        success: function (data) {
            if (data['successful'] == true) {
                alert(data['msg'])
                //$(this).parent().hide()
            }
            else {
                alert("Update unsuccessful. Please try again later")
            }
        }
    })
})


