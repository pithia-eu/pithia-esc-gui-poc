import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const workflowDetailsFileUploadRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='file_upload']");
const workflowDetailsFileUploadRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsFileUploadRadioButton.id}']`);
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");

const workflowDetailsFileExternalRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='external']");
const workflowDetailsFileExternalRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsFileExternalRadioButton.id}']`);
const workflowDetailsFileExternalTextInput = document.querySelector("input[name='workflow_details']");

const workflowDetailsRadioButtons = [
    workflowDetailsFileUploadRadioButton,
    workflowDetailsFileExternalRadioButton
];


function updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
    const isFileUploadSelected = radioButtonValue == workflowDetailsFileUploadRadioButton.value;
    if (isFileUploadSelected) {
        workflowDetailsFileUploadRadioButtonLabel.classList.add("required");
        workflowDetailsFileExternalRadioButtonLabel.classList.remove("required");
    } else {
        workflowDetailsFileUploadRadioButtonLabel.classList.remove("required");
        workflowDetailsFileExternalRadioButtonLabel.classList.add("required");
    }
    workflowDetailsFileInput.disabled = !isFileUploadSelected;
    workflowDetailsFileInput.required = isFileUploadSelected;
    workflowDetailsFileExternalTextInput.disabled = isFileUploadSelected;
    workflowDetailsFileExternalTextInput.required = !isFileUploadSelected;
}

function setupWorkflowDetailsSection() {
    const currentWorkflowDetailsSourceChoice = document.querySelector("input[name='workflow_details_file_source']:checked").value;
    updateWorkflowDetailsRelatedInputStates(currentWorkflowDetailsSourceChoice);
    workflowDetailsRadioButtons.forEach(radioButton => {
        radioButton.addEventListener("change", e => {
            updateWorkflowDetailsRelatedInputStates(e.target.value);
        });
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