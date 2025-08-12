import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
const operationTimeSection = document.getElementById("operation-time-section");


function checkAndUpdateFieldStates(operationTimeSectionInputs) {
    checkAndSetRequiredAttributesForFields(
        operationTimeSectionInputs
    );
    window.dispatchEvent(new CustomEvent("validateFields", {
        detail: {
            fieldIds: Array.from(operationTimeSectionInputs).map(input => input.id),
        },
    }));
}


export function setupOperationTimeSection() {
    const operationTimeSectionInputs = operationTimeSection.querySelectorAll("input");

    // Do initial setup in case there are already
    // some initial values in the form
    checkAndSetRequiredAttributesForFields(
        operationTimeSectionInputs
    );

    // Set event listeners for each field in the
    // operation time section
    operationTimeSectionInputs.forEach(input => {
        input.addEventListener("keyup", () => {
            checkAndUpdateFieldStates(operationTimeSectionInputs);
        });
        input.addEventListener("input", () => {
            checkAndUpdateFieldStates(operationTimeSectionInputs);
        });
    });
}