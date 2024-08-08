
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
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

window.addEventListener("load", async () => {
    setupApiInteractionMethodsSection();
    await validateOpenApiSpecificationUrl();
});