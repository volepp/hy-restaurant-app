error = false;

window.location.search
    .substring(1)
    .split("&")
    .forEach(function (item) {
        param = item.split("=");
        if (param[0] === "error") error = (param[1] == "true");
});

if (error) {
    document.getElementById("usernameInput").classList.add("is-invalid");
    document.getElementById("passwordInput").classList.add("is-invalid");
}