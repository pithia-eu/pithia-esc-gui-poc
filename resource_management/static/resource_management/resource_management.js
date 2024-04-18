const bsTooltips = document.querySelectorAll("[data-bs-toggle='tooltip']");
bsTooltips.forEach(elem => {
    new bootstrap.Tooltip(elem, {});
});