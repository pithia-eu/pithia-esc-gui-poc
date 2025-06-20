import {
    loadRelatedMetadata,
} from "/static/browse/related_metadata.js";
import {
    loadTableOfContentsElements,
} from "/static/browse/table_of_contents.js";


function enablePopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {trigger: 'hover focus'}));
}

window.addEventListener("load", async () => {
    loadTableOfContentsElements();
    enablePopovers();
    await loadRelatedMetadata();
});