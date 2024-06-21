import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    setupQualityAssessmentSection,
} from "/static/register_with_support/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupSourcesTab,
} from "/static/register_with_support/components/sources_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";
import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js";

const openApiSpecUrlInput = document.querySelector("input[name='api_specification_url']");
const apiDescriptionTextarea = document.querySelector("textarea[name='api_description']");


function checkAndSetApiInteractionMethodConditionalRequiredFields() {
    checkAndSetRequiredAttributesForFields([openApiSpecUrlInput], [apiDescriptionTextarea]);
}

function setupApiInteractionMethodsSection() {
    const fields = [
        openApiSpecUrlInput,
        apiDescriptionTextarea,
    ];
    fields.forEach(field => {
        field.addEventListener("input", () => {
            checkAndSetApiInteractionMethodConditionalRequiredFields();
        });
    });
}

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});

editorForm.addEventListener("submit", e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupLocalIdAndNamespaceRelatedEventListeners();
    const sourcesTab = setupSourcesTab();
    const relatedPartiesTable = setupRelatedPartiesTable();
    setupQualityAssessmentSection();
    setupApiInteractionMethodsSection();
    validateOpenApiSpecificationUrl();
});