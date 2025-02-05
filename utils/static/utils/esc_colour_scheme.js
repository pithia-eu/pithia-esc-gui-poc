const htmlElement = document.querySelector("html");

function switchToDarkMode(isDarkMode) {
    if (isDarkMode) {
        return htmlElement.setAttribute("data-bs-theme", "dark");
    }
    return htmlElement.setAttribute("data-bs-theme", "light");
}

if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    switchToDarkMode(true);
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    switchToDarkMode(event.matches);
});