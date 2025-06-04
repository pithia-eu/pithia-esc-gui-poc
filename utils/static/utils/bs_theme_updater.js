// Local storage
const SITE_THEME_LOCAL_STORAGE_KEY = "theme";
const LIGHT_SITE_THEME = "light";
const DARK_SITE_THEME = "dark";
const AUTO_SITE_THEME = "auto";
const META_THEME_COLOUR_LIGHT_HEX = "#E9ECEF";
const META_THEME_COLOUR_DARK_HEX = "#343A40";

// Query selectors
const htmlElement = document.querySelector("html");
const metaThemeColourElement = document.querySelector("meta[name='theme-color']");
const siteThemePicker = document.querySelector("#theme-picker");
const lightSiteThemeOption = document.querySelector("#option-theme-light");
const darkSiteThemeOption = document.querySelector("#option-theme-dark");
const autoSiteThemeOption = document.querySelector("#option-theme-auto");

const lightSiteThemeIconSelector = "#sun";
const darkSiteThemeIconSelector = "#moon-fill";
const autoSiteThemeIconSelector = "#circle-half";


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

function updateSiteThemePickerUi(siteThemeSetting) {
    const siteThemeIcon = siteThemePicker.querySelector(".dropdown-toggle svg > use");
    switch (siteThemeSetting) {
        case LIGHT_SITE_THEME:
            lightSiteThemeOption.classList.add("active");
            darkSiteThemeOption.classList.remove("active");
            autoSiteThemeOption.classList.remove("active");
            siteThemeIcon.setAttribute("xlink:href", lightSiteThemeIconSelector);
            break;
        case DARK_SITE_THEME:
            lightSiteThemeOption.classList.remove("active");
            darkSiteThemeOption.classList.add("active");
            autoSiteThemeOption.classList.remove("active");
            siteThemeIcon.setAttribute("xlink:href", darkSiteThemeIconSelector);
            break;
        default:
            lightSiteThemeOption.classList.remove("active");
            darkSiteThemeOption.classList.remove("active");
            autoSiteThemeOption.classList.add("active");
            siteThemeIcon.setAttribute("xlink:href", autoSiteThemeIconSelector);
            break;
    }
}


// Theme setters
function setLightSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, LIGHT_SITE_THEME);
    disableColourSchemePreferenceTracking();
    switchBootstrapTheme(false);
    updateSiteThemePickerUi(LIGHT_SITE_THEME);
    window.dispatchEvent(new CustomEvent("lightSiteThemeSet"));
}

function setDarkSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, DARK_SITE_THEME);
    disableColourSchemePreferenceTracking();
    switchBootstrapTheme(true);
    updateSiteThemePickerUi(DARK_SITE_THEME);
    window.dispatchEvent(new CustomEvent("darkSiteThemeSet"));
}

function setAutoSiteTheme() {
    window.localStorage.setItem(SITE_THEME_LOCAL_STORAGE_KEY, AUTO_SITE_THEME);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', trackColourSchemePreference);
    switchBootstrapTheme(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
    updateSiteThemePickerUi(AUTO_SITE_THEME);
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

lightSiteThemeOption.addEventListener("click", () => {
    setLightSiteTheme();
});

darkSiteThemeOption.addEventListener("click", () => {
    setDarkSiteTheme();
});

autoSiteThemeOption.addEventListener("click", () => {
    setAutoSiteTheme();
});

window.addEventListener("load", () => {
    setSiteThemeFromLocalStorage();
});