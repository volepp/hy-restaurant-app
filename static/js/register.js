window.location.search
    .substring(1)
    .split("&")
    .forEach(item => {
      param = item.split("=");
      if (param[0] === "errors") {
        param[1].split(",").forEach(err => {
          console.log(err)
          switch (err) {
            case "username":
              document.getElementById("usernameInput").classList.add("is-invalid");
              break;
            case "password":
              document.getElementById("passwordInput").classList.add("is-invalid");
              break;
          }
        })
      };
});