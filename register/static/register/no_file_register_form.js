const input = document.querySelector("#id_phone");
window.intlTelInput(input, {
    autoInsertDialCode: true,
    geoIpLookup: callback => {
        fetch("https://ipapi.co/json")
        .then(res => res.json())
        .then(data => callback(data.country_code))
        .catch(() => callback(""));
    },
    initialCountry: "auto",
    nationalMode: false,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.4/build/js/utils.js",
});