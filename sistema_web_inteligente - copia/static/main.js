window.onload = function() {
    alert('Este Citio Contiene Cookies.');
};

document.addEventListener("DOMContentLoaded", () => {
    const banner = document.getElementById("cookie-banner");
    const accept = document.getElementById("cookie-accept");
    const reject = document.getElementById("cookie-reject");

    if (!banner || !accept || !reject) return;

    const key = "yanko-cookie-choice";

    try {
        if (localStorage.getItem(key)) return;
    } catch (error) {
        console.warn("No se pudo leer la preferencia de cookies.");
    }

    banner.hidden = false;

    function choose(value) {
        try {
            localStorage.setItem(key, value);
        } catch (error) {
            console.warn("No se pudo guardar la preferencia.");
        }

        banner.hidden = true;
    }

    accept.addEventListener("click", () => choose("accepted"));
    reject.addEventListener("click", () => choose("rejected_optional"));
});

  
