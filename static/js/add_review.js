// Review add error handling
document.onreadystatechange = () => {
    window.location.search
        .substring(1)
        .split("&")
        .forEach(item => {
            param = item.split("=");
            if (param[0] === "reviewErrors") {
                param[1].split(",").forEach(err => {
                    switch (err) {
                        case "stars":
                            document.getElementById("reviewStars").classList.add("is-invalid");
                            break;
                        case "comment":
                            document.getElementById("reviewComment").classList.add("is-invalid");
                            break;
                }
                })
            };
    });

    // Set restaurant add tab active
    document.getElementById("add-tab").click();
}

