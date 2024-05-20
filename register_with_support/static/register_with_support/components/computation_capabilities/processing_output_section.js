import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
const requiredFields = [document.querySelector("textarea[name='processing_output_description']")];
const optionalLinkedFields = [document.querySelector("input[name='processing_output_name']")];
const allFields = [
    ...requiredFields,
    ...optionalLinkedFields,
];


function toggleConditionalRequiredFieldsIfNeeded() {
    checkAndSetRequiredAttributesForFields(
        requiredFields,
        optionalLinkedFields
    );
}

export function setupProcessingOutputSection() {
    allFields.forEach(field => {
        field.addEventListener("input", e => {
            toggleConditionalRequiredFieldsIfNeeded();
        });
    });
    toggleConditionalRequiredFieldsIfNeeded();
}