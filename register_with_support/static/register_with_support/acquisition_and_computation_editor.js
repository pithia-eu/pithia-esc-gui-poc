import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";
import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    setupCapabilityLinksTab,
} from "/static/register_with_support/components/acquisition_and_computation/capability_links_tab.js";

editorForm.addEventListener("submit", e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    await setupLocalIdAndNamespaceRelatedEventListeners();
    const capabilityLinksTab = setupCapabilityLinksTab();
});