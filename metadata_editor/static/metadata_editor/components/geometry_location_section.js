import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    dispatchValidateFieldsEvent,
} from "/static/metadata_editor/components/validation/utils/events.js";

const geometryLocationSection = editorForm.querySelector("#geometry-location-section");


function checkAndUpdateFieldStates(field, allGeometryLocationFields) {
    checkAndSetRequiredAttributesForFields(
        allGeometryLocationFields,
        allGeometryLocationFields,
    );
    if (allGeometryLocationFields.some(field => field.required)) {
        return dispatchValidateFieldsEvent([field]);
    }
    return dispatchValidateFieldsEvent(allGeometryLocationFields);
}

export function setupGeometryLocationSection() {
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
    // geolocation section
    geometryLocationInputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndUpdateFieldStates(input, allGeometryLocationFields);
        });
    });
    geometryLocationSelects.forEach(select => {
        select.addEventListener("change", () => {
            checkAndUpdateFieldStates(select, allGeometryLocationFields);
        });
    });
}