var btn = document.getElementById('rmSubmit');
var preloader = document.querySelector(".preloader");
var loader = document.getElementById('loader');
var main = document.querySelector(".main");
var form = document.forms[0];

form.addEventListener("submit", function () {
    preloader.style.display = "block";
    main.style.display = 'none';
    fetch('http://127.0.0.1:3080/remback').then((response) => {
        if (response.ok) {
            preloader.style.display = "none";
        } else {
            throw new Error("HTTP status " + response.status);
        }
    }).catch((error) => {
        console.error(error);
    });
});