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

const workflowDetailsFileSourceChoices = {}

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
    for (const choice in workflowDetailsFileSourceChoices) {
        workflowDetailsFileSourceChoices[choice].radioButton.addEventListener("change", e => {
            updateWorkflowDetailsRelatedInputStates(e.target.value);
        });
    }
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupWorkflowDetailsSection();
});