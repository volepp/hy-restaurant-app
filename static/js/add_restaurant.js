let marker = L.marker([0, 0], {"opacity": 0.0}).addTo(map);
map.on("click", (e) => {
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;
    document.getElementById("restaurantLatitude").value = lat;
    document.getElementById("restaurantLongitude").value = lng;
    marker.setLatLng([lat, lng]);
    marker.setOpacity(0.5);
});
