let marker = L.marker([0, 0], {"opacity": 0.0}).addTo(map);
map.on("click", (e) => {
    let lat = e.latlng.lat;
    let lng = e.latlng.lng;
    document.getElementById("restaurantLatitude").value = lat;
    document.getElementById("restaurantLongitude").value = lng;
    marker.setLatLng([lat, lng]);
    marker.setOpacity(0.5);
});

// Restaurant add error handling
document.addEventListener("readystatechange", () => {
    previousLatLng = [0, 0]
    window.location.search
        .substring(1)
        .split("&")
        .forEach(item => {
            param = item.split("=");
            if (param[0] === "addErrors") {
                param[1].split(",").forEach(err => {
                    switch (err) {
                        case "name":
                            document.getElementById("restaurantName").classList.add("is-invalid");
                            break;
                        case "description":
                            document.getElementById("restaurantDescription").classList.add("is-invalid");
                            break;
                        case "location":
                            document.getElementById("restaurantLatitude").classList.add("is-invalid");
                            document.getElementById("restaurantLongitude").classList.add("is-invalid");
                            break;
                }
                })
                // Set restaurant add tab active
                document.getElementById("add-tab").click();
            } else { // Restore previous form values
                switch (param[0]) {
                    // Restaurant add
                    case "name":
                        document.getElementById("restaurantName").value = param[1]
                        break
                    case "description":
                        document.getElementById("restaurantDescription").value = param[1]
                        break
                    case "lat":
                        document.getElementById("restaurantLatitude").value = param[1]
                        previousLatLng[0] = Number(param[1])
                        break
                    case "lng":
                        document.getElementById("restaurantLongitude").value = param[1]
                        previousLatLng[1] = Number(param[1])
                        break

                    // Search
                    case "restaurantKeyword":
                        document.getElementById("restaurantSearch").value = param[1]
                        break
                    case "restaurantSortBy":
                        document.getElementById("restaurantSortBy").value = param[1]
                        break
                }
            };
    });
    if (previousLatLng[0] != 0 && previousLatLng[1] != 0) {
        marker.setLatLng(previousLatLng);
        marker.setOpacity(0.5);
    }
}
);