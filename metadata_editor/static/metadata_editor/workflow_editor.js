import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js";


apiSpecificationUrlInput.addEventListener("input", async () => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    await validateOpenApiSpecificationUrl();
});

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    await validateOpenApiSpecificationUrl();
});