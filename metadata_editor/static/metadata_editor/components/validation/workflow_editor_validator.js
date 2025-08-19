import {
    BaseEditorValidator,
} from "/static/metadata_editor/components/validation/base_editor_validator.js";


export class WorkflowEditorValidator extends BaseEditorValidator {
    getCustomValidationFieldNames() {
        return ["api_specification_url", "workflow_details"];
    }
}