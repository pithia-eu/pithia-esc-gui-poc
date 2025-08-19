import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    dispatchValidateFieldsEvent,
} from "/static/metadata_editor/components/validation/utils/events.js";

const dataQualityFlagsSelect = document.querySelector("select[name='data_quality_flags']");
const metadataQualityFlagsSelect = document.querySelector("select[name='metadata_quality_flags']");
const allSelects = [
    dataQualityFlagsSelect,
    metadataQualityFlagsSelect
];


function updateQualityAssessmentConditionalRequiredFieldStates(field) {
    checkAndSetRequiredAttributesForFields(
        [dataQualityFlagsSelect],
        [metadataQualityFlagsSelect]
    );
    if (allSelects.some(select => select.required)) {
        return dispatchValidateFieldsEvent([field]);
    }
    return dispatchValidateFieldsEvent(allSelects);
}

export function setupQualityAssessmentSection() {
    updateQualityAssessmentConditionalRequiredFieldStates(allSelects);
    dataQualityFlagsSelect.addEventListener("change", () => {
        updateQualityAssessmentConditionalRequiredFieldStates([dataQualityFlagsSelect]);
    });
    metadataQualityFlagsSelect.addEventListener("change", () => {
        updateQualityAssessmentConditionalRequiredFieldStates([metadataQualityFlagsSelect]);
    });
}