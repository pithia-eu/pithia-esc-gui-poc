import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupSourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
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
    setupSourcesTab();
    setupRelatedPartiesTable();
    setupQualityAssessmentSection();
    setupApiInteractionMethodsSection();
    await validateOpenApiSpecificationUrl();
});