import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
const operationTimeSection = document.getElementById("operation-time-section");

export function setupOperationTimeSection() {
    const operationTimeSectionInputs = operationTimeSection.querySelectorAll("input");

    // Do initial setup in case there are already
    // some initial values in the form
    checkAndSetRequiredAttributesForFields(
        operationTimeSectionInputs,
        operationTimeSectionInputs,
    );

    // Set event listeners for each field in the
    // operation time section
    operationTimeSectionInputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(
                operationTimeSectionInputs,
                operationTimeSectionInputs,
            );
        });
    });
}