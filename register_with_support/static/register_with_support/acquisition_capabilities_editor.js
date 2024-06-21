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
    setupCitationSection,
} from "/static/register_with_support/components/citation_section.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";
import {
    setupQualityAssessmentSection,
} from "/static/register_with_support/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupInputOutputSection,
} from "/static/register_with_support/components/acquisition_capabilities/input_output_section.js";
import {
    setupInstrumentModePairSection,
} from "/static/register_with_support/components/acquisition_capabilities/instrument_mode_pair_section.js";

let relatedPartiesTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    setupCapabilitiesTab();
    setupInstrumentModePairSection();
    setupQualityAssessmentSection();
    setupInputOutputSection();
});