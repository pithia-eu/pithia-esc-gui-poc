import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";


window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
});

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});