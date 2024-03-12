const phoneInput = document.querySelector("#id_phone");

window.intlTelInput(phoneInput, {
    allowDropdown: false,
    autoPlaceholder: false,
    defaultToFirstCountry: false,
    nationalMode: false,
    placeholderNumberType: "FIXED_LINE",
    showFlags: false,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.4/build/js/utils.js",
});