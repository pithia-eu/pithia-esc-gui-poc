import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";

const dataQualityFlagsSelect = document.querySelector("select[name='data_quality_flags']");
const metadataQualityFlagsSelect = document.querySelector("select[name='metadata_quality_flags']");


function updateQualityAssessmentConditionalRequiredFieldStates() {
    checkAndSetRequiredAttributesForFields(
        [dataQualityFlagsSelect],
        [metadataQualityFlagsSelect]
    );
    window.dispatchEvent(new CustomEvent("validateFields", {
        detail: {
            fieldIds: [
                dataQualityFlagsSelect, metadataQualityFlagsSelect
            ].map(select => select.id),
        }
    }));
}

export function setupQualityAssessmentSection() {
    updateQualityAssessmentConditionalRequiredFieldStates();
    dataQualityFlagsSelect.addEventListener("change", updateQualityAssessmentConditionalRequiredFieldStates);
    metadataQualityFlagsSelect.addEventListener("change", updateQualityAssessmentConditionalRequiredFieldStates);
}