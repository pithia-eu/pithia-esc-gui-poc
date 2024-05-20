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
    setupQualityAssessmentSection,
} from "/static/register_with_support/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupProcessingInputsTable,
} from "/static/register_with_support/components/computation_capabilities/processing_inputs_table.js";
import {
    setupProcessingOutputSection,
} from "/static/register_with_support/components/computation_capabilities/processing_output_section.js";

let relatedPartiesTable;
let processingInputsTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    processingInputsTable = setupProcessingInputsTable();
    setupProcessingOutputSection();
    setupCapabilitiesTab();
    setupQualityAssessmentSection();
});