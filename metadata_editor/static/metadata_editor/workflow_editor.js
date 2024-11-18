import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const workflowDetailsFileExistingRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='existing']");

const workflowDetailsFileUploadRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='file_upload']");
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");

const workflowDetailsFileExternalRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='external']");
const workflowDetailsFileExternalTextInput = document.querySelector("input[name='workflow_details']");
const workflowDetailsUrlErrorList = document.querySelector("#workflow-details-url-error-list");

const workflowDetailsFileSourceChoices = {}
let workflowDetailsUrlValidationTimeout;


function setWorkflowDetailsFileSourceChoiceState(radioButtonValue, isEnabled) {
    if ('relatedInput' in workflowDetailsFileSourceChoices[radioButtonValue]) {
        workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.disabled = !isEnabled;
        workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.required = isEnabled;
    }
}

function updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
    for (const key in workflowDetailsFileSourceChoices) {
        if (key != radioButtonValue) {
            setWorkflowDetailsFileSourceChoiceState(key, false);
            continue;
        }
        setWorkflowDetailsFileSourceChoiceState(key, true);
    }
}

function validateWorkflowDetailsUrl() {
    try {
        const workflowDetailsUrl = new URL(workflowDetailsFileExternalTextInput.value);
        if (workflowDetailsUrl.hostname == 'esc.pithia.eu') {
            return {
                valid: false,
                error: "Please use the provided workflow details file input to register the details file with this workflow.",
            };
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

function resetWorkflowDetailsUrlValidationErrors() {
    workflowDetailsUrlErrorList.textContent = "";
}

function displayWorkflowDetailsValidatingProgressText() {
    workflowDetailsUrlErrorList.innerHTML = '<li class="form-text">Checking link...</li>';
}

function validateWorkflowDetailsUrlAndDisplayErrors() {
    if (!workflowDetailsFileExternalTextInput.value) {
        return;
    }
    const workflowDetailsUrlValidationResults = validateWorkflowDetailsUrl();
    if (!workflowDetailsUrlValidationResults.valid) {
        const errorListItem = document.createElement("LI");
        errorListItem.className = "form-text text-danger";
        errorListItem.textContent = workflowDetailsUrlValidationResults.error;
        workflowDetailsUrlErrorList.appendChild(errorListItem);
    }
}

function setupWorkflowDetailsSection() {
    // Group controls for each workflow details source choice
    if (workflowDetailsFileExistingRadioButton) {
        workflowDetailsFileSourceChoices[workflowDetailsFileExistingRadioButton.value] = {
            radioButton: workflowDetailsFileExistingRadioButton,
        }
    }
    workflowDetailsFileSourceChoices[workflowDetailsFileUploadRadioButton.value] = {
        radioButton: workflowDetailsFileUploadRadioButton,
        relatedInput: workflowDetailsFileInput,
    }
    workflowDetailsFileSourceChoices[workflowDetailsFileExternalRadioButton.value] = {
        radioButton: workflowDetailsFileExternalRadioButton,
        relatedInput: workflowDetailsFileExternalTextInput,
    }

    const currentWorkflowDetailsSourceChoice = document.querySelector("input[name='workflow_details_file_source']:checked").value;
    updateWorkflowDetailsRelatedInputStates(currentWorkflowDetailsSourceChoice);
    if (currentWorkflowDetailsSourceChoice === workflowDetailsFileExternalRadioButton.value) {
        validateWorkflowDetailsUrlAndDisplayErrors();
    }

    for (const choice in workflowDetailsFileSourceChoices) {
        workflowDetailsFileSourceChoices[choice].radioButton.addEventListener("change", e => {
            const radioButton = workflowDetailsFileSourceChoices[choice].radioButton;
            updateWorkflowDetailsRelatedInputStates(e.target.value);
            if (radioButton === workflowDetailsFileExternalRadioButton) {
                return validateWorkflowDetailsUrlAndDisplayErrors();
            }
            return resetWorkflowDetailsUrlValidationErrors();
        });
    }
    workflowDetailsFileExternalTextInput.addEventListener("input", () => {
        resetWorkflowDetailsUrlValidationErrors();
        if (!workflowDetailsFileExternalTextInput.value) {
            return;
        }
        displayWorkflowDetailsValidatingProgressText();
        window.clearTimeout(workflowDetailsUrlValidationTimeout);
        workflowDetailsUrlValidationTimeout = window.setTimeout(() => {
            resetWorkflowDetailsUrlValidationErrors();
            validateWorkflowDetailsUrlAndDisplayErrors();
        }, 500);
    });
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupWorkflowDetailsSection();
});