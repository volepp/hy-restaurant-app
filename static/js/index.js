var map = L.map('map').setView([60.192059, 24.945831], 10); // Set view to Helsinki
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

document.addEventListener("readystatechange", () => {
    filterGroups = []
    window.location.search
        .substring(1)
        .split("&")
        .forEach(item => {
            param = item.split("=");
            // Restore previous search form values
            switch (param[0]) {
                case "restaurantKeyword":
                    document.getElementById("restaurantSearch").value = param[1]
                    break
                case "restaurantSortBy":
                    document.getElementById("restaurantSortBy").value = param[1]
                    break
                case "filterGroups":
                    filterGroups.push(param[1])
                    break
            }
    });
    if (filterGroups.length > 0) {
        filterSelect = document.getElementById("restaurantFilterGroups")
        for (var i = 0; i < filterSelect.options.length; i++) {
            filterSelect.options[i].selected = filterGroups.indexOf(filterSelect.options[i].value) >= 0;
        }
    }
});

