import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCapabilitiesTab,
} from "/static/metadata_editor/components/capabilities_tab.js";
import {
    setupCitationSection,
} from "/static/metadata_editor/components/citation_section.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupProcessingInputsTable,
} from "/static/metadata_editor/components/computation_capabilities/processing_inputs_table.js";

let relatedPartiesTable;

const softwareReferenceSection = document.querySelector("#software-reference-section");
const softwareReferenceSectionRequiredFields = [
    softwareReferenceSection.querySelector("input[name='software_reference_citation_title']"),
    softwareReferenceSection.querySelector("input[name='software_reference_citation_publication_date']"),
];
const softwareReferenceSectionOptionalFields = [
    softwareReferenceSection.querySelector("input[name='software_reference_citation_doi']"),
    softwareReferenceSection.querySelector("textarea[name='software_reference_other_citation_details']"),
    softwareReferenceSection.querySelector("input[name='software_reference_citation_linkage_url']"),
];


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

function checkAndSetSoftwareReferenceConditionalRequiredFields() {
    checkAndSetRequiredAttributesForFields(
        softwareReferenceSectionRequiredFields,
        softwareReferenceSectionOptionalFields,
    );
}

function setupSoftwareReferenceSection() {
    checkAndSetSoftwareReferenceConditionalRequiredFields();

    const allSoftwareReferenceFields = [
        ...softwareReferenceSectionRequiredFields,
        ...softwareReferenceSectionOptionalFields,
    ];
    allSoftwareReferenceFields.forEach(field => {
        field.addEventListener("input", () => {
            checkAndSetSoftwareReferenceConditionalRequiredFields();
        });
    });
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    setupSoftwareReferenceSection();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    processingInputsTable = setupProcessingInputsTable();
    setupCapabilitiesTab();
    setupQualityAssessmentSection();
});