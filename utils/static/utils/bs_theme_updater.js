// Local storage
const SITE_THEME_LOCAL_STORAGE_KEY = "theme";
export const LIGHT_SITE_THEME = "light";
export const DARK_SITE_THEME = "dark";
export const AUTO_SITE_THEME = "auto";
const META_THEME_COLOUR_LIGHT_HEX = "#e9ecef";
const META_THEME_COLOUR_DARK_HEX = "#343a40";

// Query selectors
const htmlElement = document.querySelector("html");
const metaThemeColourElement = document.querySelector("meta[name='theme-color']");


// Utils
function switchBootstrapTheme(isDarkMode) {
    if (isDarkMode) {
        metaThemeColourElement.setAttribute("content", META_THEME_COLOUR_DARK_HEX);
        return htmlElement.setAttribute("data-bs-theme", "dark");
    }
    metaThemeColourElement.setAttribute("content", META_THEME_COLOUR_LIGHT_HEX);
    return htmlElement.setAttribute("data-bs-theme", "light");
}

function trackColourSchemePreference(event) {
    switchBootstrapTheme(event.matches);
}

function disableColourSchemePreferenceTracking() {
    window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', trackColourSchemePreference);
}


// Theme setters
export function setLightSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, LIGHT_SITE_THEME);
    disableColourSchemePreferenceTracking();
    switchBootstrapTheme(false);
    window.dispatchEvent(new CustomEvent("lightSiteThemeSet"));
}

export function setDarkSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, DARK_SITE_THEME);
    disableColourSchemePreferenceTracking();
    switchBootstrapTheme(true);
    window.dispatchEvent(new CustomEvent("darkSiteThemeSet"));
}

export function setAutoSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, AUTO_SITE_THEME);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', trackColourSchemePreference);
    switchBootstrapTheme(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
    window.dispatchEvent(new CustomEvent("autoSiteThemeSet"));
    
}


// Set event listeners
function getSiteThemeFromLocalStorage() {
    const siteThemeFromLocalStorage = window.localStorage.getItem(SITE_THEME_LOCAL_STORAGE_KEY);
    if (!siteThemeFromLocalStorage) {
        return AUTO_SITE_THEME;
    }
    return siteThemeFromLocalStorage;
}

function setSiteThemeFromLocalStorage() {
    const siteThemeFromLocalStorage = getSiteThemeFromLocalStorage();
    switch (siteThemeFromLocalStorage) {
        case LIGHT_SITE_THEME:
            setLightSiteTheme();
            break;
        case DARK_SITE_THEME:
            setDarkSiteTheme();
            break;
        default:
            setAutoSiteTheme();
            break;
    }
}

setSiteThemeFromLocalStorage();