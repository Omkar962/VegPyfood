let autocomplete;

function initAutoComplete() {
    let input = document.getElementById('id_address');
    if (!input) {
        console.error("Element with id 'id_address' not found!");
        return;
    }

    autocomplete = new google.maps.places.Autocomplete(input, {
        types: ['geocode', 'establishment'],
        componentRestrictions: { country: ['in'] }
    });

    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    let place = autocomplete.getPlace();

    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
        return;
    } else {
        console.log('Place name =>', place.name);
    }

    let geocoder = new google.maps.Geocoder();
    let address = document.getElementById('id_address').value;

    geocoder.geocode({ address: address }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            let lat = results[0].geometry.location.lat();
            let lng = results[0].geometry.location.lng();

            $('#id_latitude').val(lat);
            $('#id_longitude').val(lng);
            $('#id_address').val(address);
        }
    });

    // Loop through address components and assign them to input fields
    for (let i = 0; i < place.address_components.length; i++) {
        for (let j = 0; j < place.address_components[i].types.length; j++) {
            let addressType = place.address_components[i].types[j];
            let val = place.address_components[i].long_name;

            if (addressType === 'locality') {
                $('#id_city').val(val);
            } else if (addressType === 'administrative_area_level_1') {
                $('#id_state').val(val);
            } else if (addressType === 'country') {
                $('#id_country').val(val);
            } else if (addressType === 'postal_code') {
                $('#id_pin_code').val(val);
            }
        }
    }
}

// Ensure DOM is loaded before initializing
document.addEventListener("DOMContentLoaded", function () {
    initAutoComplete();
});
