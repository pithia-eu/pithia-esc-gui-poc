/**
 * @module bs_component_colour_schemes_updater.js
 * @description Updates Bootstrap components that do not support dark mode yet.
 */
import {
    DARK_SITE_THEME,
    getSiteThemeFromLocalStorage,
    LIGHT_SITE_THEME,
} from "/static/utils/bs_theme_updater.js";


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


// Theme setters
function updateBootstrapComponentsToSiteDarkTheme() {
    disableColourSchemePreferenceTracking();
    updateBootstrapComponentColourSchemes(true);
}

function updateBootstrapComponentsToSiteLightTheme() {
    disableColourSchemePreferenceTracking();
    updateBootstrapComponentColourSchemes(false);
}

function updateBootstrapComponentsToSiteAutoTheme() {
    updateBootstrapComponentColourSchemes(
        window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
    );
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', trackColourSchemePreference);
}

function updateBootstrapComponentsFromLocalStorage() {
    const siteThemeFromLocalStorage = getSiteThemeFromLocalStorage();
    switch (siteThemeFromLocalStorage) {
        case LIGHT_SITE_THEME:
            updateBootstrapComponentsToSiteLightTheme();
            break;
        case DARK_SITE_THEME:
            updateBootstrapComponentsToSiteDarkTheme();
            break;
        default:
            updateBootstrapComponentsToSiteAutoTheme();
            break;
    }
}


// Event listeners
window.addEventListener("lightSiteThemeSet", () => {
    updateBootstrapComponentsToSiteLightTheme();
});

window.addEventListener("darkSiteThemeSet", () => {
    updateBootstrapComponentsToSiteDarkTheme();
});

window.addEventListener("autoSiteThemeSet", () => {
    updateBootstrapComponentsToSiteAutoTheme();
});

window.addEventListener("contentLoadedAsynchronously", () => {
    updateBootstrapComponentsFromLocalStorage();
});

window.addEventListener("load", () => {
    updateBootstrapComponentsFromLocalStorage();
});