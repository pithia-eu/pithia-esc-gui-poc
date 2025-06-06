import {
    AUTO_SITE_THEME,
    DARK_SITE_THEME,
    getSiteThemeFromLocalStorage,
    LIGHT_SITE_THEME,
    setAutoSiteTheme,
    setDarkSiteTheme,
    setLightSiteTheme,
} from "/static/utils/bs_theme_updater.js";

// Query selectors
const siteThemePicker = document.querySelector("#theme-picker");
const siteThemeIcon = siteThemePicker.querySelector(".dropdown-toggle svg > use");
const lightSiteThemeOption = document.querySelector("#option-theme-light");
const darkSiteThemeOption = document.querySelector("#option-theme-dark");
const autoSiteThemeOption = document.querySelector("#option-theme-auto");

const lightSiteThemeIconSelector = "#sun";
const darkSiteThemeIconSelector = "#moon-fill";
const autoSiteThemeIconSelector = "#circle-half";


// Utils
function setActiveThemeOptionUi(activeThemeOption, inactiveThemeOptions) {
    activeThemeOption.classList.add("active");
    activeThemeOption.classList.add("fw-semibold");
    for (const inactiveOption of inactiveThemeOptions) {
        inactiveOption.classList.remove("active");
        inactiveOption.classList.remove("fw-semibold");
    }
}

function updateSiteThemePickerUi(siteThemeSetting) {
    switch (siteThemeSetting) {
        case LIGHT_SITE_THEME:
            setActiveThemeOptionUi(
                lightSiteThemeOption,
                [
                    darkSiteThemeOption,
                    autoSiteThemeOption,
                ]
            );
            siteThemeIcon.setAttribute("xlink:href", lightSiteThemeIconSelector);
            break;
        case DARK_SITE_THEME:
            setActiveThemeOptionUi(
                darkSiteThemeOption,
                [
                    lightSiteThemeOption,
                    autoSiteThemeOption,
                ]
            );
            siteThemeIcon.setAttribute("xlink:href", darkSiteThemeIconSelector);
            break;
        default:
            setActiveThemeOptionUi(
                autoSiteThemeOption,
                [
                    lightSiteThemeOption,
                    darkSiteThemeOption,
                ]
            );
            siteThemeIcon.setAttribute("xlink:href", autoSiteThemeIconSelector);
            break;
    }
}


// Set event listeners
lightSiteThemeOption.addEventListener("click", () => {
    setLightSiteTheme();
    updateSiteThemePickerUi(LIGHT_SITE_THEME);
});

darkSiteThemeOption.addEventListener("click", () => {
    setDarkSiteTheme();
    updateSiteThemePickerUi(DARK_SITE_THEME);
});

autoSiteThemeOption.addEventListener("click", () => {
    setAutoSiteTheme();
    updateSiteThemePickerUi(AUTO_SITE_THEME);
});

window.addEventListener("load", () => {
    const siteThemeFromLocalStorage = getSiteThemeFromLocalStorage();
    switch (siteThemeFromLocalStorage) {
        case LIGHT_SITE_THEME:
            updateSiteThemePickerUi(LIGHT_SITE_THEME);
            break;
        case DARK_SITE_THEME:
            updateSiteThemePickerUi(DARK_SITE_THEME);
            break;
        default:
            updateSiteThemePickerUi(AUTO_SITE_THEME);
            break;
    }
});