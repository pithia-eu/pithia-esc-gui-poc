import {
    AUTO_SITE_THEME,
    DARK_SITE_THEME,
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


// Util
function updateSiteThemePickerUi(siteThemeSetting) {
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