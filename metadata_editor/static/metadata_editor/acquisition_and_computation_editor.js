import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/metadata_editor/components/localid_validation.js";
import {
    setupCapabilityLinksTab,
} from "/static/metadata_editor/components/acquisition_and_computation/capability_links_tab.js";

editorForm.addEventListener("submit", e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    await setupLocalIdAndNamespaceRelatedEventListeners();
    const capabilityLinksTab = setupCapabilityLinksTab();
});