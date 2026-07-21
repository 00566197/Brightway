document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("cookieConsent");
    const mainContent = document.getElementById("mainContent");
    if (document.cookie.includes("cookieConsent=true")) {
        popup.style.display = "none";
        mainContent.style.display = "block";
    } else {
        popup.style.display = "flex";
        mainContent.style.display = "none";
    }
    document.getElementById("acceptCookies").onclick = function () {
        document.cookie = "cookieConsent=true; path=/; max-age=" + 60*60*24*30;
        popup.style.display = "none";
        mainContent.style.display = "block";
    };
    document.getElementById("rejectCookies").onclick = function () {
        popup.style.display = "flex";
        mainContent.style.display = "none";
    };
});
 