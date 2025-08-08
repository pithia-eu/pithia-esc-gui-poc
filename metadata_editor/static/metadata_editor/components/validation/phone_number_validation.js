import {
    iti,
    phoneInput,
} from "/static/metadata_editor/components/contact_info.js";


export const ContactInfoFieldsValidatorMixin = (Base) => class extends Base {
    getCustomValidationFieldNames() {
        const customValidationFieldNames = super.getCustomValidationFieldNames();
        customValidationFieldNames.push(phoneInput.getAttribute("name"));
        customValidationFieldNames.push("email");
        return customValidationFieldNames;
    }

    validatePhoneNumberField(field) {
        if (!field.value) {
            return this.highlightFieldAsValid(field);
        }
        if (iti.isValidNumber()) {
            return this.highlightFieldAsValid(field);
        }
        return this.highlightFieldAsInvalid(field);
    }
}