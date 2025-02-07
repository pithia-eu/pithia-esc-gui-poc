const htmlElement = document.querySelector("html");


function switchBootstrapTheme(isDarkMode) {
    if (isDarkMode) {
        return htmlElement.setAttribute("data-bs-theme", "dark");
    }
    return htmlElement.setAttribute("data-bs-theme", "light");
}

if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    switchBootstrapTheme(true);
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    switchBootstrapTheme(event.matches);
});