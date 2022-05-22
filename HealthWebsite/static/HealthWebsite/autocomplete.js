"use strict"

function autoComplete () {
    const input = document.getElementById("address");
    const options = {
        componentRestrictions: { country: "us" },
        fields: ["address_components", "geometry", "icon", "name"],
        strictBounds: false,
        types: ["address"],
        };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
}