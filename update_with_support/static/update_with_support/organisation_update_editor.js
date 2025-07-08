import {
    OrganisationEditor,
} from "/static/metadata_editor/organisation_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


window.addEventListener("load", async () => {
    const editor = await setupEditor(OrganisationEditor);
});