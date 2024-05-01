import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";

const inputOutputSection = document.getElementById("input-output-description-section");
// Input description fields
const requiredInputDescriptionFields = inputOutputSection.querySelectorAll("textarea[name='input_description']");
const optionalInputDescriptionFields = inputOutputSection.querySelectorAll("input[name='input_name']");
// Output description fields
const requiredOutputDescriptionFields = inputOutputSection.querySelectorAll("textarea[name='output_description']");
const optionalOutputDescriptionFields = inputOutputSection.querySelectorAll("input[name='output_name']");


function updateConditionalRequiredFieldStates() {
    checkAndSetRequiredAttributesForFields(
        requiredInputDescriptionFields,
        optionalInputDescriptionFields
    );
    checkAndSetRequiredAttributesForFields(
        requiredOutputDescriptionFields,
        optionalOutputDescriptionFields
    );
}

export function setupInputOutputSection() {
    updateConditionalRequiredFieldStates();

    const allInputOutputSectionFields = [
        ...requiredInputDescriptionFields,
        ...optionalInputDescriptionFields,
        ...requiredOutputDescriptionFields,
        ...optionalOutputDescriptionFields,
    ];

    allInputOutputSectionFields.forEach(field => {
        field.addEventListener("input", () => {
            updateConditionalRequiredFieldStates();
        });
    });
}
