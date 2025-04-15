import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
const phenomenonTimeSection = document.getElementById("phenomenon-time-section");

export function setupPhenomenonTimeSection() {
    const phenomenonTimeSectionInputs = phenomenonTimeSection.querySelectorAll("input");

    // Do initial setup in case there are already
    // some initial values in the form
    checkAndSetRequiredAttributesForFields(
        phenomenonTimeSectionInputs
    );

    // Set event listeners for each field in the
    // phenomenon time section
    phenomenonTimeSectionInputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(
                phenomenonTimeSectionInputs
            );
        });
    });
}