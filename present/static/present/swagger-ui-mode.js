const swaggerUIContainer = document.getElementById("swagger-ui");
const modeSelect = document.getElementById("id_mode");


function syncSwaggerModeWithUI() {
    swaggerUIContainer.dataset.mode = modeSelect.value;
}

window.addEventListener("load", () => {
    syncSwaggerModeWithUI();
});

modeSelect.addEventListener("change", () => {
    syncSwaggerModeWithUI();
});