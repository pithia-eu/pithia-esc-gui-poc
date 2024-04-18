import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
const geometryLocationSection = editorForm.querySelector("#geometry-location-section");


export function setupGeometryLocationSection() {
    // The citation title and date fields only
    // become required when other citation
    // fields are filled in.
    const geometryLocationInputs = geometryLocationSection.querySelectorAll("input[name^='geometry']");
    const geometryLocationSelects = geometryLocationSection.querySelectorAll("select");
    const allGeometryLocationFields = [
        ...geometryLocationInputs,
        ...geometryLocationSelects,
    ];

    // Do initial setup in case there are already
    // some initial values in the form
    checkAndSetRequiredAttributesForFields(
        allGeometryLocationFields,
        allGeometryLocationFields,
    );

    // Set event listeners for each field in the
    // citation section
    geometryLocationInputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(
                allGeometryLocationFields,
                allGeometryLocationFields,
            );
        });
    });
    geometryLocationSelects.forEach(select => {
        select.addEventListener("change", () => {
            checkAndSetRequiredAttributesForFields(
                allGeometryLocationFields,
                allGeometryLocationFields,
            );
        });
    });
}