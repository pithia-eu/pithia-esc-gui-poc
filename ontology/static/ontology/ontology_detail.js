import {
    setupOntologyIriCopyButtons,
} from "/static/ontology/ontology_utils_setup.js";


window.addEventListener("load", async () => {
    await setupOntologyIriCopyButtons();
});