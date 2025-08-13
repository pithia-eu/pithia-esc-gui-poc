import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
const phenomenonTimeSection = document.getElementById("phenomenon-time-section");
const phenomenonTimeSectionInputs = Array.from(phenomenonTimeSection.querySelectorAll("input"));


function checkAndUpdateFieldStates() {
    checkAndSetRequiredAttributesForFields(
        phenomenonTimeSectionInputs
    );
    window.dispatchEvent(new CustomEvent("validateFields", {
        detail: {
            fieldIds: phenomenonTimeSectionInputs.map(input => input.id),
        }
    }));
}

export function setupPhenomenonTimeSection() {
    // Do initial setup in case there are already
    // some initial values in the form
    checkAndSetRequiredAttributesForFields(
        phenomenonTimeSectionInputs
    );

    // Set event listeners for each field in the
    // phenomenon time section
    phenomenonTimeSectionInputs.forEach(input => {
        input.addEventListener("keyup", () => {
            checkAndUpdateFieldStates();
        });
        input.addEventListener("input", () => {
            checkAndUpdateFieldStates();
        });
    });
}