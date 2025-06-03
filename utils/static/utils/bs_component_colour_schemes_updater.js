/**
 * @module bs_component_colour_schemes_updater.js
 * @description Updates Bootstrap components that do not support dark mode yet.
 */


// Utils
function updateLightButtonColourSchemes(isDarkMode) {
    const lightButtons = document.querySelectorAll(".btn-light-togglable");
    if (isDarkMode) {
        return lightButtons.forEach(button => {
            button.classList.remove("btn-light");
            button.classList.add("btn-outline-light");
        });
    }
    return lightButtons.forEach(button => {
        button.classList.add("btn-light");
        button.classList.remove("btn-outline-light");
    });
}

function updateDarkOutlineButtonColourSchemes(isDarkMode) {
    const darkOutlineButtons = document.querySelectorAll(".btn-outline-dark-togglable");
    if (isDarkMode) {
        return darkOutlineButtons.forEach(button => {
            button.classList.remove("btn-outline-dark");
            button.classList.add("btn-outline-light");
        });
    }
    return darkOutlineButtons.forEach(button => {
        button.classList.add("btn-outline-dark");
        button.classList.remove("btn-outline-light");
    });
}

function updateBootstrapComponentColourSchemes(isDarkMode) {
    updateLightButtonColourSchemes(isDarkMode);
    updateDarkOutlineButtonColourSchemes(isDarkMode);
}

function trackColourSchemePreference(event) {
    updateBootstrapComponentColourSchemes(event.matches);
}

function disableColourSchemePreferenceTracking() {
    window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', trackColourSchemePreference);
}


// Event listeners
window.addEventListener("lightSiteThemeSet", () => {
    disableColourSchemePreferenceTracking();
    updateBootstrapComponentColourSchemes(false);
});

window.addEventListener("darkSiteThemeSet", () => {
    disableColourSchemePreferenceTracking();
    updateBootstrapComponentColourSchemes(true);
});

window.addEventListener("autoSiteThemeSet", () => {
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        updateBootstrapComponentColourSchemes(true);
    }
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', trackColourSchemePreference);
});