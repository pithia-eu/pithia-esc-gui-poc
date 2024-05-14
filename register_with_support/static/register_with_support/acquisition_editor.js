import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
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

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    const capabilityLinksTab = setupCapabilityLinksTab();
});