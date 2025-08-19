import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/metadata_editor/components/localid_validation.js";


window.addEventListener("load", async () => {
    await setupLocalIdAndNamespaceRelatedEventListeners();
});