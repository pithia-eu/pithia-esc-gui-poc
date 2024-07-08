import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";

const inputOutputSection = document.getElementById("input-output-description-section");
// Input description fields
const requiredInputDescriptionFields = inputOutputSection.querySelectorAll("textarea[name='input_description']");
const optionalInputDescriptionFields = inputOutputSection.querySelectorAll("input[name='input_name']");


function updateConditionalRequiredFieldStates() {
    checkAndSetRequiredAttributesForFields(
        requiredInputDescriptionFields,
        optionalInputDescriptionFields
    );
}

export function setupInputOutputSection() {
    updateConditionalRequiredFieldStates();

    const allInputOutputSectionFields = [
        ...requiredInputDescriptionFields,
        ...optionalInputDescriptionFields,
    ];

    allInputOutputSectionFields.forEach(field => {
        field.addEventListener("input", () => {
            updateConditionalRequiredFieldStates();
        });
    });
}
