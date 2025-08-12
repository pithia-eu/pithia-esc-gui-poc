import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";


export  class BaseEditorValidator {
    setup() {
        this.setupOnNewFieldsAddedEventListener();
        this.setupLiveValidationForFields(this.getOnInputValidationFields());
        this.setupOnBlurValidationForFields(this.getOnBlurValidationFields());
        this.setupLiveValidationForSelects(this.getOnInputValidationSelects());
        this.setupOnCallValidationForFields();
    }

    getCustomValidationFieldNames() {
        return [];
    }

    #getCustomValidationFieldsSelector() {
        return this.getCustomValidationFieldNames().map(fieldName => `[name="${fieldName}"]`).join(", ");
    }

    #getNotCustomValidationFieldsSelectorOrBlankStringIfEmpty() {
        const customValidationFieldsSelector = this.#getCustomValidationFieldsSelector();
        if (!customValidationFieldsSelector) {
            return "";
        }
        return `:not(${customValidationFieldsSelector})`;
    }

    getOnBlurValidationFieldNames() {
        return [];
    }

    #getOnBlurValidationFieldsSelector() {
        return this.getOnBlurValidationFieldNames().map(fieldName => `[name="${fieldName}"]`).join(", ");
    }

    #getNotOnBlurValidationFieldsSelectorOrBlankStringIfEmpty() {
        const onBlurValidationFieldsSelector = this.#getOnBlurValidationFieldsSelector();
        if (!onBlurValidationFieldsSelector) {
            return "";
        }
        return `:not(${onBlurValidationFieldsSelector})`;
    }

    getOnInputValidationFields() {
        const notCustomValidationFieldsSelectorOrBlankString = this.#getNotCustomValidationFieldsSelectorOrBlankStringIfEmpty();
        const notOnBlurValidationFieldsSelectorOrBlankString = this.#getNotOnBlurValidationFieldsSelectorOrBlankStringIfEmpty();
        return Array.from(editorForm.querySelectorAll(
            `input${notOnBlurValidationFieldsSelectorOrBlankString}${notCustomValidationFieldsSelectorOrBlankString},
            textarea${notOnBlurValidationFieldsSelectorOrBlankString}${notCustomValidationFieldsSelectorOrBlankString}`
        ));
    }

    getOnBlurValidationFields() {
        const onBlurValidationFieldsSelector = this.#getOnBlurValidationFieldsSelector();
        if (!onBlurValidationFieldsSelector) {
            return [];
        }
        return Array.from(editorForm.querySelectorAll(onBlurValidationFieldsSelector));
    }

    getOnInputValidationSelects() {
        return [];
    }

    setupLiveValidationForFields(fields) {
        for (const field of fields) {
            field.addEventListener("input", e => {
                this.validateField(field);
            });
        }
    }

    setupOnBlurValidationForFields(fields) {
        for (const field of fields) {
            field.addEventListener("blur", e => {
                this.validateField(field);
            });
        }
    }

    setupLiveValidationForSelects(selects) {
        for (const select of selects) {
            select.addEventListener("input", e => {
                this.validateSelect(select);
            });
        }
    }

    setupOnCallValidationForFields() {
        window.addEventListener("validateFields", e => {
            const fieldIds = e.detail.fieldIds;
            const fieldsSelector = fieldIds.map(fieldId => `#${fieldId}`).join(", ");
            const fields = document.querySelectorAll(fieldsSelector);
            this.validateFields(fields);
        });
    }

    setupOnNewFieldsAddedEventListener() {
        window.addEventListener("newOnInputValidationFieldsAdded", e => {
            const newFieldIds = e.detail;
            const newFields = document.querySelectorAll(newFieldIds.map(id => `#${id}`).join(","));
            this.setupLiveValidationForFields(newFields);
        });

        window.addEventListener("newOnBlurValidationFieldsAdded", e => {
            const newFieldIds = e.detail;
            const newFields = document.querySelectorAll(newFieldIds.map(id => `#${id}`).join(","));
            this.setupOnBlurValidationForFields(newFields);
        });

        window.addEventListener("newSelectsAdded", e => {

        });
    }

    #getWrapperForField(field) {
        return document.querySelector(`.field-wrapper[data-field="${field.id}"]`);
    }

    highlightFieldAsValid(field) {
        const fieldWrapper = this.#getWrapperForField(field);
        if (fieldWrapper) {
            fieldWrapper.classList.remove("is-invalid")
        }
        const tsControl = document.querySelector(`#${field.id} + .ts-wrapper`);
        if (tsControl) {
            tsControl.classList.remove("is-invalid");
        }
        return field.classList.remove("is-invalid");
    }
    
    highlightFieldAsInvalid(field) {
        const fieldWrapper = this.#getWrapperForField(field);
        if (fieldWrapper) {
            fieldWrapper.classList.add("is-invalid")
        }
        const tsControl = document.querySelector(`#${field.id} + .ts-wrapper`);
        if (tsControl) {
            tsControl.classList.add("is-invalid");
        }
        field.classList.add("is-invalid");
        const fieldFeedbackElement = document.querySelector(`#invalid-feedback-${field.id}`);
        return fieldFeedbackElement.textContent = field.validationMessage;
    }

    validateField(field) {
        const isFieldValid = field.checkValidity();
        if (isFieldValid) {
            return this.highlightFieldAsValid(field);
        }
        return this.highlightFieldAsInvalid(field);
    }

    validateFields(fields) {
        for (const field of fields) {
            this.validateField(field);
        }
    }

    validateSelect(select) {
        const isFieldValid = select.checkValidity();
        const tsWrapper = document.querySelector(`#${select.id} + .ts-wrapper`);
        if (isFieldValid) {
            this.highlightFieldAsValid(select);
            return tsWrapper.classList.remove("is-invalid");
        }
        this.highlightFieldAsInvalid(select);
        return tsWrapper.classList.add("is-invalid");
    }

    validateSelects(selects) {
        for (const select of selects) {
            this.validateSelect(select);
        }
    }
}