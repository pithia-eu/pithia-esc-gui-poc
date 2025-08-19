import {
    iti,
    phoneInput,
} from "/static/metadata_editor/components/contact_info.js";


export const ContactInfoFieldsValidatorMixin = (Base) => class extends Base {
    setup() {
        super.setup();
        // Error map: https://intl-tel-input.com/examples/validation-practical.html
        this.phoneValidationErrorMap = [
            "Invalid number",
            "Invalid country code",
            "Too short",
            "Too long",
            "Invalid number"
        ];
        this.phoneInput = phoneInput;
        this.setupPhoneInputValidation();
    }

    getCustomValidationFieldNames() {
        const customValidationFieldNames = super.getCustomValidationFieldNames();
        customValidationFieldNames.push(phoneInput.getAttribute("name"));
        customValidationFieldNames.push("email_address");
        return customValidationFieldNames;
    }

    validatePhoneInput() {
        if (!this.phoneInput.value) {
            return this.highlightFieldAsValid(this.phoneInput);
        }
        if (iti.isValidNumber()) {
            return this.highlightFieldAsValid(this.phoneInput);
        }
        const errorCode = iti.getValidationError();
        const errorMsg = this.phoneValidationErrorMap[errorCode] || "Invalid number";
        this.phoneInput.setCustomValidity(errorMsg);
        return this.highlightFieldAsInvalid(this.phoneInput);
    }

    setupPhoneInputValidation() {
        this.phoneInput.addEventListener("input", () => {
            this.validatePhoneInput();
        });
    }
}