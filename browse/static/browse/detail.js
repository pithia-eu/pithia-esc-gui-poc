import {
    loadRelatedMetadata,
} from "/static/browse/related_metadata.js";


function enablePopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {trigger: 'hover focus'}));
}

window.addEventListener("load", async () => {
    enablePopovers();
    await loadRelatedMetadata();
});