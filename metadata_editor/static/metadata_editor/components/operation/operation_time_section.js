import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    dispatchValidateFieldsEvent,
} from "/static/metadata_editor/components/validation/utils/events.js";

const operationTimeSection = document.getElementById("operation-time-section");


function checkAndUpdateFieldStates(operationTimeSectionInputs) {
    checkAndSetRequiredAttributesForFields(
        operationTimeSectionInputs
    );
    dispatchValidateFieldsEvent(operationTimeSectionInputs);
}


export function setupOperationTimeSection() {
    const operationTimeSectionInputs = Array.from(operationTimeSection.querySelectorAll("input"));

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