import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupCapabilitiesTab,
} from "/static/register_with_support/components/capabilities_tab.js";
import {
    setupInstrumentModePairSection,
} from "/static/register_with_support/components/acquisition_capabilities/instrument_mode_pair_section.js";

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupCapabilitiesTab();
    setupInstrumentModePairSection();
});