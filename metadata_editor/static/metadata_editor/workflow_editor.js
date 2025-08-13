import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    checkIfEscUrl,
} from "/static/metadata_editor/components/url_format_checker.js";
import {
    WorkflowEditorValidator,
} from "/static/metadata_editor/components/validation/workflow_editor_validator.js";


export class WorkflowEditor extends BaseEditor {
    setup() {
        super.setup();
        this.workflowDetailsFileExistingRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='existing']");

        this.workflowDetailsFileUploadRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='file_upload']");
        this.workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");
        
        this.workflowDetailsFileExternalRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='external']");
        this.workflowDetailsFileExternalTextInput = document.querySelector("input[name='workflow_details']");
        this.workflowDetailsUrlErrorList = document.querySelector("#workflow-details-url-error-list");
        
        this.workflowDetailsFileSourceChoices = {}
        this.workflowDetailsUrlValidationTimeout;

        setupWizardManualAndAutoSave();
        this.setupWorkflowDetailsSection();
        this.setupUrlInputValidation();
    }

    getValidator() {
        return new WorkflowEditorValidator();
    }

    setWorkflowDetailsFileSourceChoiceState(radioButtonValue, isEnabled) {
        if ('relatedInput' in this.workflowDetailsFileSourceChoices[radioButtonValue]) {
            this.workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.disabled = !isEnabled;
            this.workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.required = isEnabled;
        }
    }
    
    updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
        for (const key in this.workflowDetailsFileSourceChoices) {
            if (key != radioButtonValue) {
                this.setWorkflowDetailsFileSourceChoiceState(key, false);
                continue;
            }
            this.setWorkflowDetailsFileSourceChoiceState(key, true);
        }
    }
    
    validateWorkflowDetailsUrl() {
        try {
            const isWorkflowDetailsUrlInternal = checkIfEscUrl(this.workflowDetailsFileExternalTextInput.value);
            if (isWorkflowDetailsUrlInternal) {
                return {
                    valid: false,
                    error: "Please use the provided workflow details file input to register the details file with this workflow.",
                }
            }
        } catch (error) {
            console.error(error);
            return {
                valid: false,
                error: "Please enter a URL",
            };
        }
        return {
            valid: true,
        };
    }
    
    resetWorkflowDetailsUrlValidationErrors() {
        this.workflowDetailsUrlErrorList.textContent = "";
    }
    
    displayWorkflowDetailsValidatingProgressText() {
        this.workflowDetailsUrlErrorList.innerHTML = '<li class="form-text">Checking link...</li>';
    }
    
    validateWorkflowDetailsUrlAndDisplayErrors() {
        if (!this.workflowDetailsFileExternalTextInput.value) {
            return;
        }
        const workflowDetailsUrlValidationResults = this.validateWorkflowDetailsUrl();
        if (!workflowDetailsUrlValidationResults.valid) {
            this.workflowDetailsFileExternalTextInput.classList.add("is-invalid");
            const errorListItem = document.createElement("LI");
            errorListItem.className = "form-text text-danger";
            errorListItem.textContent = workflowDetailsUrlValidationResults.error;
            this.workflowDetailsUrlErrorList.appendChild(errorListItem);
        }
    }
    
    setupWorkflowDetailsSection() {
        // Group controls for each workflow details source choice
        if (this.workflowDetailsFileExistingRadioButton) {
            this.workflowDetailsFileSourceChoices[this.workflowDetailsFileExistingRadioButton.value] = {
                radioButton: this.workflowDetailsFileExistingRadioButton,
            }
        }
        this.workflowDetailsFileSourceChoices[this.workflowDetailsFileUploadRadioButton.value] = {
            radioButton: this.workflowDetailsFileUploadRadioButton,
            relatedInput: this.workflowDetailsFileInput,
        }
        this.workflowDetailsFileSourceChoices[this.workflowDetailsFileExternalRadioButton.value] = {
            radioButton: this.workflowDetailsFileExternalRadioButton,
            relatedInput: this.workflowDetailsFileExternalTextInput,
        }
    
        const currentWorkflowDetailsSourceChoice = document.querySelector("input[name='workflow_details_file_source']:checked").value;
        this.updateWorkflowDetailsRelatedInputStates(currentWorkflowDetailsSourceChoice);
        if (currentWorkflowDetailsSourceChoice === this.workflowDetailsFileExternalRadioButton.value) {
            this.validateWorkflowDetailsUrlAndDisplayErrors();
        }
    
        for (const choice in this.workflowDetailsFileSourceChoices) {
            this.workflowDetailsFileSourceChoices[choice].radioButton.addEventListener("change", e => {
                const radioButton = this.workflowDetailsFileSourceChoices[choice].radioButton;
                this.updateWorkflowDetailsRelatedInputStates(e.target.value);
                if (radioButton === this.workflowDetailsFileExternalRadioButton) {
                    this.validateWorkflowDetailsUrlAndDisplayErrors();
                    return window.dispatchEvent(new CustomEvent("validateFields", {
                        detail: {
                            fieldIds: [
                                this.workflowDetailsFileInput,
                                this.workflowDetailsFileExternalTextInput,
                            ].map(field => field.id),
                        }
                    }));
                }
                this.resetWorkflowDetailsUrlValidationErrors();
                return window.dispatchEvent(new CustomEvent("validateFields", {
                    detail: {
                        fieldIds: [
                            this.workflowDetailsFileInput,
                            this.workflowDetailsFileExternalTextInput,
                        ].map(field => field.id),
                    }
                }));
            });
        }
        this.workflowDetailsFileExternalTextInput.addEventListener("input", () => {
            this.resetWorkflowDetailsUrlValidationErrors();
            if (!this.workflowDetailsFileExternalTextInput.value) {
                return;
            }
            this.displayWorkflowDetailsValidatingProgressText();
            window.clearTimeout(this.workflowDetailsUrlValidationTimeout);
            this.workflowDetailsUrlValidationTimeout = window.setTimeout(() => {
                this.resetWorkflowDetailsUrlValidationErrors();
                this.validateWorkflowDetailsUrlAndDisplayErrors();
            }, 500);
        });
    }

    setupUrlInputValidation() {
        const workflowOpenApiSpecificationUrlInput = document.querySelector("input[name='api_specification_url']");
        workflowOpenApiSpecificationUrlInput.addEventListener("input", () => {
            const openApiSpecificationUrlFeedbackElement = document.querySelector(".api-specification-url-status-validation");
            const validator = this.getValidator();
            const value = workflowOpenApiSpecificationUrlInput.value;
            if (value.length > 0) {
                openApiSpecificationUrlFeedbackElement.classList.remove("d-none");
                return validator.highlightFieldAsValid(workflowOpenApiSpecificationUrlInput);
            }
            openApiSpecificationUrlFeedbackElement.classList.add("d-none");
            return validator.validateField(workflowOpenApiSpecificationUrlInput);
        });

        const workflowDetailsUrlInput = document.querySelector("input[name='workflow_details']");
        workflowDetailsUrlInput.addEventListener("input", () => {
            const feedbackElement = document.querySelector("#workflow-details-url-error-list");
            const validator = this.getValidator();
            const value = workflowDetailsUrlInput.value;
            if (value.length > 0) {
                feedbackElement.classList.remove("d-none");
                return validator.highlightFieldAsValid(workflowDetailsUrlInput);
            }
            feedbackElement.classList.add("d-none");
            return validator.validateField(workflowDetailsUrlInput);
        });
    }
}