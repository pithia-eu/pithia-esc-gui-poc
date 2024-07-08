import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/metadata_editor/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    await setupLocalIdAndNamespaceRelatedEventListeners();
});