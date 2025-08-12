import {
    BaseEditorValidator,
} from "/static/metadata_editor/components/validation/base_editor_validator.js";
import {
    ContactInfoFieldsValidatorMixin,
} from "/static/metadata_editor/components/validation/phone_number_validation.js";


export class OrganisationEditorValidator extends ContactInfoFieldsValidatorMixin(BaseEditorValidator) {
}